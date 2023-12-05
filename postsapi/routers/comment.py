from fastapi import APIRouter, HTTPException
from postsapi.models.comment import UserComment, UserCommentIn
import postsapi.routers.post
from postsapi.database import comments_table, database

router = APIRouter()

async def get_post_comments(post_id):
  query = comments_table.select().where(comments_table.c.post_id == post_id)
  return await database.fetch_all(query)

@router.post('/', response_model=UserComment)
async def create_comment(comment: UserCommentIn):
  data = comment.dict()
  post = await postsapi.routers.post.check_if_post_available(data['post_id'])
  if not post:
    raise HTTPException(status_code=404, detail="Post not available")
  query = comments_table.insert().values(data)
  last_record_id = await database.execute(query)
  new_comment = {**data, "id": last_record_id}
  return new_comment