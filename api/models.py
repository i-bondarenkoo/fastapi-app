# модели которые относятся к обработке запроса
import re
import uuid

from fastapi import HTTPException
from pydantic import BaseModel, EmailStr, field_validator, ConfigDict


LETTER_MATCH_PATTERN = re.compile(r"^[а-яА-Яa-zA-Z\-]+$")


class TunedModel(BaseModel):
    class Config:
        # это свойство конвертирует объекты к виду json(даже если объект не словарь)
        model_config = ConfigDict(from_attributes=True)


# модель ответа
class ShowUser(TunedModel):
    user_id: uuid.UUID
    name: str
    surname: str
    email: EmailStr
    is_active: bool


# модель обработки входящего запроса(post запрос)
class UserCreate(BaseModel):
    name: str
    surname: str
    email: EmailStr

    # валидация имени
    @field_validator("name")
    def validate_name(cls, value):
        if not LETTER_MATCH_PATTERN.match(value):
            raise HTTPException(
                status_code=422, detail="Name should contains only letters"
            )
        return value

    # валидация фамилии
    @field_validator("surname")
    def validate_surname(cls, value):
        if not LETTER_MATCH_PATTERN.match(value):
            raise HTTPException(
                status_code=422, detail="Name should contains only letters"
            )
        return value
