from fastapi import APIRouter, Depends
from apps.auth.routes import current_user, super_user
from gpt.main import ChatCompletion
import apps.core.schemas as scheme
import time
from apps.auth.models import User, Credit
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from db.setup import get_async_session
from apps.auth.orm import CreditOrm


coreRouter = APIRouter()
router = coreRouter


@router.post("/chat/completion", tags=["generate"])
async def chat_completion(
    item: scheme.ChatCompletionCreate,
    user: User = Depends(current_user),
    session: AsyncSession = Depends(get_async_session)
    ):

    credit = await CreditOrm.getByUser(userId=user.id)

    amount = await CreditOrm.spend(id=credit.id, sum_=15)
    
    request = item.dict()

    request["amount"] = amount
    request["used"] = 15
        
    chat = ChatCompletion(**request)

    start_time = time.perf_counter()

    output = chat.complete()

    end_time = time.perf_counter()
    execution_time = end_time - start_time

    return {"message": output, "exc_time": execution_time}