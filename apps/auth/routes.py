from fastapi import APIRouter, Request, Depends
import apps.auth.schemas as scheme
import uuid
from .models import User
from fastapi_users import FastAPIUsers
from .manager import get_user_manager
from .setup import auth_backend

router = APIRouter()


fastapi_users = FastAPIUsers[User, uuid.UUID](
    get_user_manager,
    [auth_backend],
)


current_user = fastapi_users.current_user()


# Custom endpoints


@router.post("/apitoken")
async def add_token(item: scheme.ApiTokenScheme, user: User = Depends(current_user)):

    return {"user_id": user.id}





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