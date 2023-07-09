import uuid
from typing import Optional

from fastapi import Depends, Request
from fastapi_users import BaseUserManager, UUIDIDMixin
from .models import User, get_user_db, Credit
from db.setup import async_session_maker
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import insert

class UserManager(UUIDIDMixin, BaseUserManager[User, uuid.UUID]):

    async def on_after_register(
        self, user: User, 
        request: Optional[Request] = None
        ):

        async with async_session_maker() as session:
            query = insert(Credit).values(userId=user.id)
            await session.execute(query)
            await session.commit()




async def get_user_manager(user_db=Depends(get_user_db)):
    yield UserManager(user_db)