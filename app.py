from fastapi import FastAPI
import uvicorn
from apps.auth.routes import router

app = FastAPI()
app.include_router(router, prefix="/api")


if __name__ == "__main__":
    uvicorn.run("app:app", host="0.0.0.0", port=8000, reload=True, workers=3)
