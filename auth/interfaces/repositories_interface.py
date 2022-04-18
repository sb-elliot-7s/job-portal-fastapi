from abc import ABC, abstractmethod
from typing import Optional

from users.models import UserAccount


class AuthRepositoriesInterface(ABC):

    @abstractmethod
    async def get_user_by_email(self, email: str) -> UserAccount: pass

    @abstractmethod
    async def save_user(self, email: str, password: str, username: Optional[str], user_type_name: str) -> UserAccount: pass
