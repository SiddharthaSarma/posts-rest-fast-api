from fastapi import APIRouter, HTTPException
from postsapi.models.post import UserPost, UserPostIn
from postsapi.models.comment import UserPostComments, UserComment
import postsapi.routers.comment
from postsapi.database import posts_table, database

router = APIRouter()

async def check_if_post_available(post_id):
  query = posts_table.select().where(posts_table.c.id == post_id)
  return await database.fetch_one(query)

@router.get('/', response_model=list[UserPost])
async def get_posts():
  query = posts_table.select()
  return await database.fetch_all(query)

@router.post('/', response_model=UserPost)
async def create_post(post: UserPostIn):
  data = post.dict()
  query = posts_table.insert().values(data)
  last_record_id = await database.execute(query)
  return {**data, 'id': last_record_id}

@router.get('/{post_id}/comments')
async def get_post_comments(post_id: int):
  return await postsapi.routers.comment.get_post_comments(post_id)

@router.get('/{post_id}', response_model=UserPostComments)
async def get_post_with_comments(post_id: int):
  post = await check_if_post_available(post_id)
  if not post:
    raise HTTPException(status_code=404, detail='Post not found')
  return {"post": post, "comments": await get_post_comments(post_id)}