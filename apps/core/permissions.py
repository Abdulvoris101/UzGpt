from fastapi import Request, HTTPException
from apps.auth.orm import ApiTokenOrm

async def is_authenticated_or_token(request: Request, user):

    if user is None:
        authentication_header = request.headers.get("Authorization")
        
        if authentication_header is None or not authentication_header.startswith("Bearer "):
            raise HTTPException(status_code=401, detail="Unauthorized")

        token = authentication_header.split(" ")[1]
        apitoken = await ApiTokenOrm.getByToken(token=token)

        if apitoken is None:
            raise HTTPException(status_code=400, detail="Invalid token")

        return apitoken.userId
        
        
    return user.id
