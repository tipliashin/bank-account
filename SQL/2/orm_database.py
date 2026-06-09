"""
Пример работы с SQLAlchemy ORM.
Модели: User (пользователь) и Account (счёт).
Связь "один-ко-многим" с каскадным удалением.
"""
from sqlalchemy import create_engine, Column, Integer, String, Float, ForeignKey, update, select
from sqlalchemy.orm import declarative_base, relationship, Session

# 1. Базовый класс для моделей
Base = declarative_base()

# 2. Определяем модели
class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    name = Column(String(50), nullable=False, unique=True)

    # Связь с таблицей accounts
    # back_populates создаёт двунаправленную связь: user.accounts и account.owner
    # cascade='all, delete-orphan' означает, что при удалении пользователя
    # все его счета будут автоматически удалены.
    accounts = relationship(
        'Account',
        back_populates='owner',
        cascade='all, delete-orphan'
    )

    def __repr__(self):
        return f"<User(id={self.id}, name='{self.name}')>"


class Account(Base):
    __tablename__ = 'accounts'

    id = Column(Integer, primary_key=True)
    balance = Column(Float, default=0.0)
    owner_id = Column(Integer, ForeignKey('users.id'))

    # Связь с таблицей users
    owner = relationship('User', back_populates='accounts')

    def __repr__(self):
        return f"<Account(id={self.id}, balance={self.balance}, owner_id={self.owner_id})>"


# 3. Создаём движок (engine) и сессию
# Здесь база данных будет в файле bank_orm.db в текущей папке
DATABASE_URL = "sqlite:///bank_orm.db"
engine = create_engine(DATABASE_URL, echo=False)  # echo=True покажет SQL-запросы

# 4. Функция main, где выполняется вся демонстрация
def main():
    # Создаём таблицы (если их ещё нет)
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)

    # Создаём сессию для работы с объектами
    with Session(engine) as session:
        # ---------- ДОБАВЛЕНИЕ ДАННЫХ ----------
        # Создаём пользователей
        anna = User(name='Анна')
        ivan = User(name='Иван')
        session.add_all([anna, ivan])
        session.flush()  # чтобы получить id пользователей до создания счетов

        # Создаём счета и привязываем к пользователям
        acc1 = Account(balance=500.0, owner=anna)
        acc2 = Account(balance=1500.0, owner=anna)
        acc3 = Account(balance=300.0, owner=ivan)
        session.add_all([acc1, acc2, acc3])
        session.commit()

        # ---------- ЗАПРОСЫ ----------
        print("=== Все счета пользователя Анна ===")
        # Способ 1: через relationship
        user_anna = session.query(User).filter_by(name='Анна').first()
        for acc in user_anna.accounts:
            print(f"  Счёт #{acc.id}, баланс: {acc.balance}")

        print("\n=== Все пользователи и их счета ===")
        users = session.query(User).all()
        for user in users:
            print(f"Пользователь: {user.name}")
            for acc in user.accounts:
                print(f"  Счёт #{acc.id}, баланс: {acc.balance}")

        # ---------- ОБНОВЛЕНИЕ БАЛАНСА ----------
        print("\n=== Увеличение баланса счетов Анны на 10% ===")
        user_anna = session.query(User).filter_by(name='Анна').first()
        subquery = select(Account.id).join(User).where(User.name == 'Анна').scalar_subquery()

        # Выполняем обновление
        session.execute(
            update(Account).
            where(Account.id.in_(subquery)).
            values(balance=Account.balance * 1.1)
        )
        session.commit()
        # ---------- УДАЛЕНИЕ ПОЛЬЗОВАТЕЛЯ ----------
        print("\n=== Удаление пользователя Иван (и его счетов) ===")
        user_ivan = session.query(User).filter_by(name='Иван').first()
        session.delete(user_ivan)  # благодаря cascade счета удалятся автоматически
        session.commit()

        print("Оставшиеся пользователи и их счета:")
        for user in session.query(User).all():
            print(f"  {user.name}: {[acc.balance for acc in user.accounts]}")

        print("\nГотово! Таблицы созданы, данные изменены.")

if __name__ == "__main__":
    main()