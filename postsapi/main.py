from fastapi import FastAPI
from postsapi.routers.post import router as PostsRouter
from postsapi.routers.comment import router as CommentRouter
from contextlib import asynccontextmanager
from .database import database

@asynccontextmanager
async def lifespan(app: FastAPI):
  await database.connect()
  yield
  await database.disconnect()


app = FastAPI(lifespan=lifespan)
app.include_router(PostsRouter, prefix="/posts")
app.include_router(CommentRouter, prefix="/comments")
