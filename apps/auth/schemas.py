import uuid

from fastapi_users import schemas
from datetime import timezone, datetime
from typing import Optional
from pydantic import BaseModel


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
    createdAt: Optional[datetime]


class ApiTokenRead(BaseModel):
    id: uuid.UUID
    token: str
    userId: uuid.UUID
    name: str


class ApiTokenCreate(BaseModel):
    name: str

class CreditRead(BaseModel):
    amount: int

class CreditUpdate(BaseModel):
    userId: uuid.UUID
    amount: int