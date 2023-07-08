from fastapi import APIRouter, Depends
import apps.auth.schemas as scheme
import uuid
from .models import User, ApiToken
from fastapi_users import FastAPIUsers
from .manager import get_user_manager
from .setup import auth_backend
from sqlalchemy.ext.asyncio import AsyncSession
from db.setup import get_async_session
from sqlalchemy import insert, values, select, delete
import typing
from utils import JsonResponse

router = APIRouter()


fastapi_users = FastAPIUsers[User, uuid.UUID](
    get_user_manager,
    [auth_backend],
)


current_user = fastapi_users.current_user()


# Custom endpoints

#  Api Token

@router.post("/apitoken", response_model=scheme.ApiTokenRead, tags=["token"])
async def add_token(
    item: scheme.ApiTokenCreate,
    user: User = Depends(current_user),
    session: AsyncSession = Depends(get_async_session)
    ):

    obj = ApiToken(userId=user.id, name=item.name)

    await obj.save(session)

    return scheme.ApiTokenRead(**obj.__dict__)


@router.get("/apitoken", tags=["token"])
async def get_tokens(
    user: User = Depends(current_user),
    session: AsyncSession = Depends(get_async_session),
    ):

    query = select(ApiToken).where(ApiToken.userId == user.id)
    result = await session.execute(query)

    return result.scalars().all()


@router.delete("/apitoken/{pk}", tags=["token"])
async def delete_token(
    pk: uuid.UUID,
    user: User = Depends(current_user),
    session: AsyncSession = Depends(get_async_session),
    ):
    query = delete(ApiToken).where((ApiToken.id == pk) & (ApiToken.userId == user.id))
    await session.execute(query)
    
    await session.commit()

    return JsonResponse(message="Api token succesfully deleted", status_code=200)






# Include fastapi-users routers

router.include_router(
    fastapi_users.get_auth_router(auth_backend),
    prefix="/api/auth",
    tags=["auth"],
)

router.include_router(
    fastapi_users.get_register_router(scheme.UserRead, scheme.UserCreate),
    prefix="/api/auth",
    tags=["auth"],
)

router.include_router(
    fastapi_users.get_users_router(scheme.UserRead, scheme.UserUpdate),
    prefix="/users",
    tags=["users"],
)
