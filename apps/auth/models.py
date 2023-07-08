from fastapi_users.db import SQLAlchemyBaseUserTableUUID, SQLAlchemyUserDatabase
from db.setup import Base, get_async_session
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import Column, String, DateTime, ForeignKey, BigInteger
from sqlalchemy.dialects.postgresql import UUID

import uuid
import secrets


class User(SQLAlchemyBaseUserTableUUID, Base):
    firstName = Column(String)
    lastName = Column(String)
    createdAt = Column(DateTime(timezone=True))


class ApiToken(Base):
    __tablename__ = "apitoken"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    token = Column(String, default=secrets.token_hex, unique=True)
    userId = Column(UUID, ForeignKey(User.id))
    name = Column(String)

    def __init__(self, userId, name):
        self.userId = userId
        self.name = name

    async def save(self, session):
        session.add(self)
        await session.commit()


class Credit(Base):
    __tablename__ = "credit"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    amount = Column(BigInteger, default=5000)
    userId = Column(UUID, ForeignKey(User.id))

    def __init__(self, userId, amount=None):
        if amount is not None:
            self.amount = amount
                    
        self.userId = userId

    async def save(self, session):
        session.add(self)
        await session.commit()


async def get_user_db(session: AsyncSession = Depends(get_async_session)):
    yield SQLAlchemyUserDatabase(session, User)

