from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, EmailStr
import uvicorn
from fastapi import APIRouter
from sqlalchemy import Column, Boolean, String
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, DeclarativeBase, mapped_column, Mapped

import settings
from sqlalchemy.dialects.postgresql import UUID
import uuid
import re

# -------------------------
# общее взаимодействие я БД
engine = create_async_engine(settings.REAL_DATABASE_URL, future=True, echo=True)

# объект асинхронной сессии
async_session = sessionmaker(engine, expire_on_commit=False)
# --------------------------------------------------------


# ---------------------------------
# блок с моделями БД ОРМ
# базовый класс, от которого наследуются наши классы-таблицы
class Base(DeclarativeBase):
    pass


class User(Base):
    __tablename__ = "users"

    user_id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    # user_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name: Mapped[str] = mapped_column(String(35), nullable=False)
    surname: Mapped[str] = mapped_column(String(35), nullable=False)
    email: Mapped[str] = mapped_column(String(35), nullable=False, unique=True)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)


# ---------------------------------------
# блок бизнес-логики
# здесь все взаимодействия связанные с пользователем
class UserDAL:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create_user(self, name: str, surname: str, email: str) -> User:
        new_user = User(
            name=name,
            surname=surname,
            email=email,
        )
        self.session.add(new_user)
        await self.session.flush()
        return new_user


# ---------------------------
# блок с моделями API

LETTER_MATCH_PATTERN = re.compile(r"^[а-яА-Яа-zA-Z\-]+$")
