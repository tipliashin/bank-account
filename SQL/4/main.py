from typing import List
from fastapi import FastAPI, Depends, HTTPException
from pydantic import BaseModel, ConfigDict
from sqlalchemy import create_engine, Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import declarative_base, Session, sessionmaker, relationship, joinedload

# ---------- Настройка базы данных ----------
# URL базы данных SQLite (файл bank.db в текущей папке)
DATABASE_URL = "sqlite:///./bank.db"

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


# ---------- Модель SQLAlchemy (таблица accounts) ----------
class AccountModel(Base):
    __tablename__ = "accounts"

    id = Column(Integer, primary_key=True, index=True)
    owner = relationship('User', back_populates='accounts')
    balance = Column(Float, default=0.0)
    owner_id = Column(Integer, ForeignKey('users.id'))


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    name = Column(String(50), nullable=False, unique=True)
    email = Column(String(50), nullable=False, unique=True)
    accounts = relationship(
        'AccountModel',
        back_populates='owner',
        cascade='all, delete-orphan'
    )

# Удаляем все таблицы перед созданием (только для разработки!)
# Base.metadata.drop_all(bind=engine)
# Создаём таблицы в базе данных (если их ещё нет)
Base.metadata.create_all(bind=engine)


# ---------- Pydantic-схемы (для запросов и ответов) ----------
class CreateAccountRequest(BaseModel):
    owner_id: int
    balance: float = 0.0


class CreateUserRequest(BaseModel):
    name: str
    email: str

class AccountResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    balance: float
    owner_id: int   # вместо owner_name

class UserResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    name: str
    email: str
    accounts: List[AccountResponse] = []


# ---------- Инициализация FastAPI ----------
app = FastAPI(title="Bank Account API")


# ---------- Зависимость для получения сессии БД ----------
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# ---------- CRUD-эндпоинты ----------

@app.post("/accounts", response_model=AccountResponse)
def create_account(request: CreateAccountRequest, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == request.owner_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    account = AccountModel(owner_id=request.owner_id, balance=request.balance)
    db.add(account)
    db.commit()
    db.refresh(account)
    return account  # FastAPI использует AccountResponse


@app.post("/users", response_model=UserResponse)
def create_user(request: CreateUserRequest, db: Session = Depends(get_db)):
    user = User(name=request.name, email=request.email)
    db.add(user)
    db.commit()
    db.refresh(user)  # получаем id, сгенерированный базой
    return user


@app.get("/accounts/{account_id}", response_model=AccountResponse)
def get_account(account_id: int, db: Session = Depends(get_db)):
    account = db.query(AccountModel).filter(AccountModel.id == account_id).first()
    if not account:
        raise HTTPException(status_code=404, detail="Account not found")
    return account

@app.get("/users/{user_id}", response_model=UserResponse)
def get_user(user_id: int, db: Session = Depends(get_db)):
    user = db.query(User).options(joinedload(User.accounts)).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@app.put("/accounts/{account_id}", response_model=AccountResponse)
def update_balance(account_id: int, balance: float, db: Session = Depends(get_db)):
    account = db.query(AccountModel).filter(AccountModel.id == account_id).first()
    if not account:
        raise HTTPException(status_code=404, detail="Account not found")
    account.balance = balance
    db.commit()
    db.refresh(account)
    return account


@app.delete("/accounts/{account_id}")
def delete_account(account_id: int, db: Session = Depends(get_db)):
    account = db.query(AccountModel).filter(AccountModel.id == account_id).first()
    if not account:
        raise HTTPException(status_code=404, detail="Account not found")
    db.delete(account)
    db.commit()
    return {"message": "Account deleted"}


@app.delete("/users/{user_id}")
def delete_user(user_id: int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    db.delete(user)
    db.commit()
    return {"message": "User deleted"}


@app.get("/accounts", response_model=list[AccountResponse])
def list_accounts(db: Session = Depends(get_db)):
    return db.query(AccountModel).all()


@app.get("/users", response_model=list[UserResponse])
def list_users(db: Session = Depends(get_db)):
    return db.query(User).options(joinedload(User.accounts)).all()