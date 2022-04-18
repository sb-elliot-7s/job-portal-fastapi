from .interfaces.password_interface import PasswordServiceInterface
from passlib.context import CryptContext


class PasswordService(PasswordServiceInterface):

    def __init__(self, context: CryptContext):
        self._context = context

    async def verify_password(self, plain_password: str, hashed_password: str) -> bool:
        return self._context.verify(plain_password, hashed_password)

    async def get_hashed_password(self, password: str) -> str:
        return self._context.hash(password)
