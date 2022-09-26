from app.db.repositories.base import BaseRepository
from app.db.queries.queries import queries
from app.db.errors import EntityDoesNotExist
from app.models.domain.users import UserInDB

class UsersRepository(BaseRepository):
    async def get_user_by_email(self, *, email: str) -> UserInDB:
        user_row = await queries.get_user_by_email(self.connection, email=email)
        if user_row:
            return UserInDB(**user_row)
        raise EntityDoesNotExist(f"user with email {email} does not exist")

    async def get_user_by_username(self, *, username: str) -> UserInDB:
        user_row = await queries.get_user_by_username(
            self.connection,
            username=username,
        )
        if user_row:
            return UserInDB(**user_row)
        raise EntityDoesNotExist(
            f"user with username {username} does not exist",
        )
# TODO: