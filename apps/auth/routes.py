from fastapi import APIRouter, Depends, HTTPException
import apps.auth.schemas as scheme
import uuid
from .models import User, ApiToken, Credit
from .manager import get_user_manager
from fastapi_users import FastAPIUsers
from .setup import auth_backend
from sqlalchemy.ext.asyncio import AsyncSession
from db.setup import get_async_session
from sqlalchemy import insert, values, select, delete, update
import typing
from utils import JsonResponse


authRouter = APIRouter()
router = authRouter

fastapi_users = FastAPIUsers[User, uuid.UUID](
    get_user_manager,
    [auth_backend],
)


current_user = fastapi_users.current_user()
current_optional_user = fastapi_users.current_user(optional=True)
super_user = fastapi_users.current_user(superuser=True)


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


# Amount

@router.get("/amount", tags=["amount"])
async def get_amount(
    user: User = Depends(current_user),
    session: AsyncSession = Depends(get_async_session)
    ):
    
    query = select(Credit).where(Credit.userId == user.id)

    res = await session.execute(query)

    return res.scalar()



@router.patch("/amount/patch", tags=["amount"])
async def update_amount(
    item: scheme.CreditUpdate,
    user: User = Depends(super_user),
    session: AsyncSession = Depends(get_async_session),
    ) -> scheme.CreditUpdate:
    
    is_exist = select(Credit).filter_by(userId=item.userId)

    query = update(Credit).where(Credit.userId == item.userId).values(amount=item.amount)

    res = await session.execute(is_exist)

    if res.scalar() is None:
        raise HTTPException(status_code=400, detail="User doesn't exist!")

    
    await session.execute(query)
    await session.commit()

    return item






# Include fastapi-users routers

router.include_router(
    fastapi_users.get_auth_router(auth_backend),
    prefix="/auth",
    tags=["auth"],
)

router.include_router(
    fastapi_users.get_register_router(scheme.UserRead, scheme.UserCreate),
    prefix="/auth",
    tags=["auth"],
)

router.include_router(
    fastapi_users.get_users_router(scheme.UserRead, scheme.UserUpdate),
    prefix="/users",
    tags=["users"],
)
