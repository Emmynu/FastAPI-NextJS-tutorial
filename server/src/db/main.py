from sqlmodel import create_engine, SQLModel
from sqlalchemy.ext.asyncio import AsyncEngine
from src.config import config
from src.db.models import Post
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlalchemy.orm import sessionmaker


engine = AsyncEngine(
    create_engine(
    url = config.DATABASE_URL,
    echo = True
))


# create a conn to our db
async def initDB():
    async with engine.begin() as conn:
        Post
        await conn.run_sync(SQLModel.metadata.create_all)


async def session() -> AsyncSession:
    
    Session = sessionmaker(
        bind=engine,
        class_= AsyncSession,
        expire_on_commit=False
    )

    async with Session() as s:
        yield s