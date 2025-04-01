from fastapi import FastAPI, HTTPException

from pydantic import BaseModel, EmailStr, field_validator, ConfigDict
import uvicorn
from fastapi import APIRouter
from sqlalchemy import Boolean, String
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.orm import sessionmaker, DeclarativeBase, mapped_column, Mapped
from api.handlers import user_router as user_router
import settings
from sqlalchemy.dialects.postgresql import UUID
import uuid
import re

# -------------------------
# общее взаимодействие я БД
# engine = create_async_engine(settings.REAL_DATABASE_URL, echo=True)

# # объект асинхронной сессии
# # при вызове он создает сессию с БД
# # async_session = sessionmaker(engine, expire_on_commit=False, class_=AsyncSession
# async_session = async_sessionmaker(engine, expire_on_commit=False)
# # --------------------------------------------------------


# ---------------------------------
# блок с моделями БД ОРМ
# базовый класс, от которого наследуются наши классы-таблицы
# class Base(DeclarativeBase):
#     pass


# class UserOrm(Base):
#     __tablename__ = "users"

#     user_id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
#     # user_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
#     name: Mapped[str] = mapped_column(String(35), nullable=False)
#     surname: Mapped[str] = mapped_column(String(35), nullable=False)
#     email: Mapped[str] = mapped_column(String(35), nullable=False, unique=True)
#     is_active: Mapped[bool] = mapped_column(Boolean, default=True)


# ---------------------------------------
# # блок бизнес-логики
# # здесь все взаимодействия связанные с пользователем
# class UserDAL:
#     def __init__(self, session: AsyncSession):
#         self.session = session

#     async def create_user(self, name: str, surname: str, email: str) -> UserOrm:
#         new_user = UserOrm(
#             name=name,
#             surname=surname,
#             email=email,
#         )
#         self.session.add(new_user)
#         await self.session.flush()
#         return new_user


# ---------------------------
# блок с моделями API

# LETTER_MATCH_PATTERN = re.compile(r"^[а-яА-Яa-zA-Z\-]+$")


# class TunedModel(BaseModel):
#     class Config:
#         # это свойство конвертирует объекты к виду json(даже если объект не словарь)
#         model_config = ConfigDict(from_attributes=True)


# # модель ответа
# class ShowUser(TunedModel):
#     user_id: uuid.UUID
#     name: str
#     surname: str
#     email: EmailStr
#     is_active: bool


# # модель обработки входящего запроса(post запрос)
# class UserCreate(BaseModel):
#     name: str
#     surname: str
#     email: EmailStr

#     # валидация имени
#     @field_validator("name")
#     def validate_name(cls, value):
#         if not LETTER_MATCH_PATTERN.match(value):
#             raise HTTPException(
#                 status_code=422, detail="Name should contains only letters"
#             )
#         return value

#     # валидация фамилии
#     @field_validator("surname")
#     def validate_surname(cls, value):
#         if not LETTER_MATCH_PATTERN.match(value):
#             raise HTTPException(
#                 status_code=422, detail="Name should contains only letters"
#             )
#         return value


# ---------------------------
# блок с роутерами api
app = FastAPI(title="Учебный проект (надеюсь у меня получится)")

# user_router = APIRouter()


# async def _create_new_user(body: UserCreate) -> ShowUser:
#     async with async_session() as session:
#         async with session.begin():
#             user_dal = UserDAL(session)
#             user = await user_dal.create_user(
#                 name=body.name,
#                 surname=body.surname,
#                 email=body.email,
#             )
#             return ShowUser(
#                 user_id=user.user_id,
#                 name=user.name,
#                 surname=user.surname,
#                 email=user.email,
#                 is_active=user.is_active,
#             )


# @user_router.post("/", response_model=ShowUser)
# async def create_user(body: UserCreate):
#     return await _create_new_user(body)


main_api_router = APIRouter()
main_api_router.include_router(
    user_router,
    prefix="/user",
    tags=["User"],
)
app.include_router(main_api_router)

if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)

    # 21 минута
