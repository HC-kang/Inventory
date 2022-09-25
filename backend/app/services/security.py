from passlib.context import CryptContext
import bcrypt

PWD_CONTEXT = CryptContext(schemas=["bcrypt"], deprecated="auto")


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return PWD_CONTEXT.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    return PWD_CONTEXT.hash(password)


def generate_salt() -> str:
    return bcrypt.gensalt().decode()
