from fastapi import APIRouter, Depends, Request
from apps.auth.routes import current_user, super_user, current_optional_user
from gpt.main import ChatCompletion, Completion
import apps.core.schemas as scheme
import time
from apps.auth.models import User, Credit
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from db.setup import get_async_session
from apps.auth.orm import CreditOrm
from .permissions import is_authenticated_or_token


coreRouter = APIRouter()
router = coreRouter


@router.post("/completion/chat", tags=["generate"])
async def chat_completion(
    item: scheme.ChatCompletionCreate,
    request: Request,
    user: User = Depends(current_optional_user),
    session: AsyncSession = Depends(get_async_session)
    ):

    userId = await is_authenticated_or_token(request, user)

    credit = await CreditOrm.getByUser(userId=userId)

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


@router.post("/completion", tags=["generate"])
async def completion(
    item: scheme.CompletionCreate,
    request: Request,
    user: User = Depends(current_optional_user),
    session: AsyncSession = Depends(get_async_session)
    ):

    userId = await is_authenticated_or_token(request, user)

    credit = await CreditOrm.getByUser(userId=userId)

    amount = await CreditOrm.spend(id=credit.id, sum_=5)
    
    request = item.dict()

    request["amount"] = amount
    request["used"] = 5
    
    chat = Completion(**request)

    start_time = time.perf_counter()

    output = chat.complete()

    end_time = time.perf_counter()
    execution_time = end_time - start_time

    return {"message": output, "exc_time": execution_time}