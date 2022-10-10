from typing import Optional

from fastapi import Query, Path

from app.models.schemas.articles import (
    DEFAULT_ARTICLES_LIMIT,
    DEFAULT_ARTICLES_OFFSET,
    ArticlesFilters,
)
from app.models.domain.users import User


def get_articles_filters(
    tag: Optional[str] = None,
    author: Optional[str] = None,
    favorited: Optional[str] = None,
    limit: int = Query(DEFAULT_ARTICLES_LIMIT, ge=1),
    offset: int = Query(DEFAULT_ARTICLES_OFFSET, ge=0),
) -> ArticlesFilters:
    return ArticlesFilters(
        tag=tag,
        author=author,
        favorited=favorited,
        limit=limit,
        offset=offset
    )


async def get_article_by_slug_from_path(
    slug: str = Path(..., min_length=1),
    user: Optional[User] = Depends()
)