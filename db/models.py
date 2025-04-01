from sqlalchemy.orm import Mapped, mapped_column, DeclarativeBase
from sqlalchemy import String, Boolean
from sqlalchemy.dialects.postgresql import UUID
import uuid


# блок с моделями БД ОРМ
# базовый класс, от которого наследуются наши классы-таблицы
class Base(DeclarativeBase):
    pass


class UserOrm(Base):
    __tablename__ = "users"

    user_id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    # user_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name: Mapped[str] = mapped_column(String(35), nullable=False)
    surname: Mapped[str] = mapped_column(String(35), nullable=False)
    email: Mapped[str] = mapped_column(String(35), nullable=False, unique=True)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
