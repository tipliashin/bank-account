from typing import List, AsyncGenerator, Optional
from fastapi import FastAPI, Depends, HTTPException
from pydantic import BaseModel, ConfigDict
from sqlalchemy import Column, Integer, String, Float, ForeignKey, select
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.orm import declarative_base, relationship, joinedload
from tasks import send_welcome_email
import os
from dotenv import load_dotenv
load_dotenv()  # загружает переменные из .env в окружение

# ---------- Настройка асинхронной БД ----------
DATABASE_URL = os.getenv("DATABASE_URL")
engine = create_async_engine(DATABASE_URL, echo=False)
AsyncSessionLocal = async_sessionmaker(engine, expire_on_commit=False)
Base = declarative_base()


# ---------- Модели ----------
class Account(Base):
    __tablename__ = "accounts"

    id = Column(Integer, primary_key=True, index=True)
    balance = Column(Float, default=0.0)
    owner_id = Column(Integer, ForeignKey('users.id'))
    owner = relationship('User', back_populates='accounts')


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    name = Column(String(50), nullable=False, unique=True)
    email = Column(String(50), nullable=False, unique=True)
    phone = Column(String(20), nullable=True)
    accounts = relationship(
        'Account',
        back_populates='owner',
        cascade='all, delete-orphan'
    )


# ---------- Pydantic-схемы ----------
class CreateAccountRequest(BaseModel):
    owner_id: int
    balance: float = 0.0


class CreateUserRequest(BaseModel):
    name: str
    email: str
    phone: Optional[str] = None  # разрешаем None


class AccountResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    balance: float
    owner_id: int


class UserResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    name: str
    email: str
    phone: Optional[str] = None  # разрешаем None
    accounts: List[AccountResponse] = []


# ---------- FastAPI ----------
app = FastAPI(title="Async Bank API")


# ---------- Асинхронная зависимость для сессии ----------
async def get_db() -> AsyncGenerator[AsyncSession, None]:
    async with AsyncSessionLocal() as session:
        yield session


# ---------- CRUD ----------

@app.post("/users", response_model=UserResponse)
async def create_user(request: CreateUserRequest, db: AsyncSession = Depends(get_db)):
    user = User(name=request.name, email=request.email, phone=request.phone)
    db.add(user)
    await db.commit()
    # Перезагружаем пользователя с joinedload, чтобы загрузить пустой список счетов
    stmt = select(User).options(joinedload(User.accounts)).where(User.id == user.id)
    result = await db.execute(stmt)
    user = result.scalars().first()

    # Отправляем фоновую задачу (не ждём результат)
    send_welcome_email.delay(user.name, user.email)

    return user


@app.post("/accounts", response_model=AccountResponse)
async def create_account(request: CreateAccountRequest, db: AsyncSession = Depends(get_db)):
    # Проверим, существует ли пользователь
    user = await db.get(User, request.owner_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    account = Account(owner_id=request.owner_id, balance=request.balance)
    db.add(account)
    await db.commit()
    await db.refresh(account)
    return account


@app.get("/users/{user_id}", response_model=UserResponse)
async def get_user(user_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        select(User).options(joinedload(User.accounts)).where(User.id == user_id)
    )
    user = result.scalars().first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@app.get("/users", response_model=List[UserResponse])
async def list_users(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(User).options(joinedload(User.accounts)))
    return result.scalars().unique().all()


@app.get("/accounts/{account_id}", response_model=AccountResponse)
async def get_account(account_id: int, db: AsyncSession = Depends(get_db)):
    account = await db.get(Account, account_id)
    if not account:
        raise HTTPException(status_code=404, detail="Account not found")
    return account


@app.put("/accounts/{account_id}", response_model=AccountResponse)
async def update_balance(account_id: int, balance: float, db: AsyncSession = Depends(get_db)):
    account = await db.get(Account, account_id)
    if not account:
        raise HTTPException(status_code=404, detail="Account not found")
    account.balance = balance
    await db.commit()
    await db.refresh(account)
    return account


@app.put("/users/{user_id}", response_model=UserResponse)
async def update_phone(user_id: int, phone: Optional[str] = None, db: AsyncSession = Depends(get_db)):
    # Сначала загружаем пользователя со счетами, чтобы избежать MissingGreenlet
    stmt = select(User).options(joinedload(User.accounts)).where(User.id == user_id)
    result = await db.execute(stmt)
    user = result.scalars().first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    user.phone = phone
    await db.commit()
    await db.refresh(user)
    return user


@app.delete("/accounts/{account_id}")
async def delete_account(account_id: int, db: AsyncSession = Depends(get_db)):
    account = await db.get(Account, account_id)
    if not account:
        raise HTTPException(status_code=404, detail="Account not found")
    await db.delete(account)
    await db.commit()
    return {"message": "Account deleted"}


@app.delete("/users/{user_id}")
async def delete_user(user_id: int, db: AsyncSession = Depends(get_db)):
    user = await db.get(User, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    await db.delete(user)
    await db.commit()
    return {"message": "User deleted"}


@app.on_event("startup")
async def startup_event():
    # Создаём таблицы при старте (для разработки)
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


@app.on_event("shutdown")
async def shutdown_event():
    await engine.dispose()
