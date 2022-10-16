from asyncpg import Connection

from app.db.repositories.base import BaseRepository
# from app.db.repositories.profiles


class CommentsRepository(BaseRepository):
    def __init__(self, conn: Connection) -> None:
        super().__init__(conn)
        self._profiles_repo = ProfilesRepository(conn)