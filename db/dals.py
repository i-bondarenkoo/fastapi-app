from sqlalchemy.ext.asyncio import AsyncSession
from db.models import UserOrm


# блок бизнес-логики
# здесь все взаимодействия связанные с пользователем
class UserDAL:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create_user(self, name: str, surname: str, email: str) -> UserOrm:
        new_user = UserOrm(
            name=name,
            surname=surname,
            email=email,
        )
        self.session.add(new_user)
        await self.session.flush()
        return new_user
