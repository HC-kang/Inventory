from typing import Sequence, Dict, Optional

from asyncpg import Connection, Record


class TagsQueriesMixin:
    async def get_all_tags(self, conn: Connection) -> Record: ...
    async def create_new_tags(
        self, conn: Connection, tags: Sequence[Dict[str, str]]
    ) -> None: ...


class UserQueriesMixin:
    async def get_user_by_email(self, conn: Connection, *, email: str) -> Record: ...
    async def get_user_by_username(
        self, conn: Connection, *, username: str
    ) -> Record: ...
    async def create_new_user(
        self,
        conn: Connection,
        *,
        username: str,
        email: str,
        salt: str,
        hashed_password: str
    ) -> Record: ...
    async def update_user_by_username(
        self,
        conn: Connection,
        *,
        username: str,
        new_username: str,
        new_email: str,
        new_salt: str,
        new_password: str,
        new_bio: Optional[str],
        new_image: Optional[str]
    ) -> Record: ...


class ProfilesQueriesMixin:
    async def is_user_following_for_another(
        self, conn: Connection, *, follower_username: str, following_username: str
    ) -> Record: ...
    async def subscribe_user_to_another(
        self, conn: Connection, *, follower_username: str, following_username: str
    ) -> None: ...
    async def unsubscribe_user_from_another(
        self, conn: Connection, *, follower_username: str, following_username: str
    ) -> None: ...


class Queries(
    TagsQueriesMixin,
    UserQueriesMixin,
    ProfilesQueriesMixin,
): ...

queries: Queries
