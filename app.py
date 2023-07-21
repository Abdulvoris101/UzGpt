from fastapi import FastAPI, Request
import uvicorn
from apps.auth.routes import authRouter
from apps.core.routes import coreRouter
from gpt.main import modelRouter
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="Uzgpt", description="Documentation of Uzgpt")



app.add_middleware(
    CORSMiddleware,
    allow_credentials=True,
    allow_origins=["http://127.0.0.1:3000/", "http://127.0.0.1:3000"],
    allow_methods=["*"],  # You can restrict to specific methods, e.g., ["GET", "POST"]
    allow_headers=["*"],  # You can restrict specific headers, e.g., ["Authorization"]
)

app.include_router(authRouter, prefix="/api")
app.include_router(coreRouter, prefix="/api")
app.include_router(modelRouter)



if __name__ == "__main__":
    uvicorn.run("app:app", host="0.0.0.0", port=8000)
