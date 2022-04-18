from abc import ABC, abstractmethod


class TokenServiceInterface(ABC):

    @abstractmethod
    async def create_token(self, email: str, secret_key: str, algorithm: str, token_type: str, exp_time: int) -> str: pass

    @abstractmethod
    async def decode_access_token(self, access_token: str, secret_key: str, algorithm: str) -> dict: pass

    @abstractmethod
    async def decode_refresh_token(self, refresh_token: str, secret_key: str, algorithm: str): pass
