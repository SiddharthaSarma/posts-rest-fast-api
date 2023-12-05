from pydantic import BaseModel
from .post  import UserPost

class UserCommentIn(BaseModel):
  body: str
  post_id: int

class UserComment(UserCommentIn):
  id: int

class UserPostComments(BaseModel):
  post: UserPost
  comments: list[UserComment]