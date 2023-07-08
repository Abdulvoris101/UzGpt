from fastapi import FastAPI
import uvicorn
from apps.auth.routes import authRouter
from apps.core.routes import coreRouter
from gpt.main import modelRouter

app = FastAPI(title="Uzgpt", description="Documentation of Uzgpt")

app.include_router(authRouter, prefix="/api")
app.include_router(coreRouter, prefix="/api")
app.include_router(modelRouter)


if __name__ == "__main__":
    uvicorn.run("app:app", host="0.0.0.0", port=8000)
