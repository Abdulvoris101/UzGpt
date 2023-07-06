from fastapi_users.db import SQLAlchemyBaseUserTableUUID, SQLAlchemyUserDatabase
from db.setup import Base, get_async_session
from fastapi_users.db import SQLAlchemyUserDatabase
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import Column, String, DateTime

class User(SQLAlchemyBaseUserTableUUID, Base):
    firstName = Column(String)
    lastName = Column(String)
    createdAt = Column(DateTime)



async def get_user_db(session: AsyncSession = Depends(get_async_session)):
    yield SQLAlchemyUserDatabase(session, User)