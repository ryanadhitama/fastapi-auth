from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from router.auth import router as auth_router

app = FastAPI()

app.include_router(auth_router)

@app.get("/")
def root():
    return {"ping": "pong!"}
