from fastapi import FastAPI

from . import models
from .database import engine

from .routers import post, user, authentication,vote

from .config import settings
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

origins = ['https://www.google.com']

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(post.router)
app.include_router(user.router)
app.include_router(authentication.router)
app.include_router(vote.router)

@app.get("/")  
async def root():
    return {"message": "Hello World"}
