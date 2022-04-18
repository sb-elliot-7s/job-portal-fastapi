from abc import ABC, abstractmethod
from fastapi import UploadFile


class SaveImageFileInterface(ABC):
    @abstractmethod
    async def read_image(self, filename: str): pass

    @abstractmethod
    async def save_image(self, file: UploadFile, filename: str): pass

    @abstractmethod
    async def delete_image(self, filename: str): pass
