from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

engine = create_async_engine("sqlite+aiosqlite:///./app.db", echo=True)

Base = declarative_base()

async_session = sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)
session = async_session()
