from fastapi import APIRouter, Request, Depends
from .schemas import UserRead

router = APIRouter()

@router.post("/users")
async def hello(item: UserRead):
    
    return item