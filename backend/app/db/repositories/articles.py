from typing import Optional, Sequence

from asyncpg import Connection

from app.models.domain.users import User
from app.models.domain.articles import Ar
from app.db.repositories.base import BaseRepository

AUTHOR_USERNAME_ALIAS = "author_username"
SLUG_ALIAS = "slug"

CAMEL_OR_SNAKE_CASE_TO_WORDS = r"^[a-z\d_\-]+|[A-Z]\d_\-][^A-Z\d_\-]*"

class ArticlesRepository(BaseRepository):
    def __init__(self, conn: Connection) -> None:
        super().__init__(conn)
        # self._profiles_repo = 

    async def create_article(
        self,
        *,
        slug: str,
        title: str,
        description: str,
        body: str,
        author: User,
        tags: Optional[Sequence[str]] = None,
    ) -> Article:
        