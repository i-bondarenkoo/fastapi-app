from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker

import settings

engine = create_async_engine(settings.REAL_DATABASE_URL, echo=True)

# объект асинхронной сессии
# при вызове он создает сессию с БД
# async_session = sessionmaker(engine, expire_on_commit=False, class_=AsyncSession
async_session = async_sessionmaker(engine, expire_on_commit=False)


# получает асинхронный объект сессии
# и выдает его как генератор, затем останавливается на строку yield session и ждет следующего вызова
async def get_db():
    try:
        session: AsyncSession = async_session()
        yield session
    finally:
        await session.close()
