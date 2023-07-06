import uuid

from fastapi_users import schemas
from datetime import datetime

class UserRead(schemas.BaseUser[uuid.UUID]):
    firstName: str
    lastName: str
    createdAt: datetime

class UserCreate(schemas.BaseUserCreate):
    firstName: str
    lastName: str
    createdAt: datetime


class UserUpdate(schemas.BaseUserUpdate):
    firstName: str
    lastName: str
    createdAt: datetime