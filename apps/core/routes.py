from fastapi import APIRouter, Depends, Request
from apps.auth.routes import current_user, super_user, current_optional_user
from gpt.main import ChatCompletion, Completion
import apps.core.schemas as scheme
import time
from apps.auth.models import User, Credit
from sqlalchemy.ext.asyncio import AsyncSession
from db.setup import get_async_session
from apps.auth.orm import CreditOrm
from .permissions import is_authenticated_or_token
from sse_starlette.sse import EventSourceResponse
import json


coreRouter = APIRouter()
router = coreRouter


@router.post("/completion/chat", tags=["generate"])
async def chat_completion(
    item: scheme.ChatCompletionCreate,
    request: Request,
    user: User = Depends(current_optional_user)
    ):

    userId = await is_authenticated_or_token(request, user)

    credit = await CreditOrm.getByUser(userId=userId)

    amount = await CreditOrm.spend(id=credit.id, sum_=15)
    
    requestData = item.dict()

    requestData["amount"] = amount
    requestData["used"] = 15
        
    chat = ChatCompletion(**requestData)

    data = await chat.complete()

    if item.stream:
        if data is not None:
            async def event_stream():
                async for item in data:
                    yield json.dumps(item)

            return EventSourceResponse(event_stream(), media_type="application/json")
    
    return data


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
    
    requestData = item.dict()

    requestData["amount"] = amount
    requestData["used"] = 5
    
    chat = Completion(**requestData)
    
    data = await chat.complete()

    if item.stream:
        if data is not None:
            async def event_stream():
                async for item in data:
                    yield json.dumps(item)

            return EventSourceResponse(event_stream(), media_type="application/json")
    
    return data
