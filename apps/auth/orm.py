from .models import Credit, User, ApiToken
from sqlalchemy import select, update, delete
from sqlalchemy.ext.asyncio import AsyncSession
from db.setup import async_session_maker
from fastapi import HTTPException

class CreditOrm:

    @classmethod
    async def getByUser(self, userId):
        async with async_session_maker() as session:
            query = select(Credit).where(Credit.userId == userId)
            credit = await session.execute(query)
            
            return credit.scalar_one_or_none()

    
    @classmethod
    def is_enough(cls, total, spend):
        return True if total >= spend else HTTPException(status_code=400, detail="You have no money left. Please top up your account")
    
    @classmethod
    async def spend(self, id, sum_):
        async with async_session_maker() as session:
            
            obj = await session.get(Credit, {"id": id})

            self.is_enough(total=obj.amount, spend=sum_)
            
            amount = obj.amount - sum_

            query = update(Credit).where(Credit.id == id).values(amount=amount)

            await session.execute(query)
            await session.commit()

            
            
            return amount