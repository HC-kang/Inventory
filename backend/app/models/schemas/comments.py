from typing import List

from app.models.schemas.rwschema import RWSchema
from app.models.domain.comments import Comment


class ListOfCommentsInResponse(RWSchema):
    comments: List[Comment]


class CommentInResponse(RWSchema):
    comment: Comment


class CommentInCreate(RWSchema):
    body: str
