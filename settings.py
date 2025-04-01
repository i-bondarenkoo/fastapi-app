from email.policy import default
from envparse import Env

env = Env()

# подключение к базе данных (ссылка)
REAL_DATABASE_URL = env.str(
    "REAL_DATABASE_URL",
    default="postgresql+asyncpg://postgres:postgres@localhost:5434/postgres",
)
