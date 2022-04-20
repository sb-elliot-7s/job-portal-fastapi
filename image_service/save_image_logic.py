from uuid import uuid4
import aiofiles
from aiofiles import os as _os
from fastapi import UploadFile
from .interfaces.image_service_interface import SaveImageFileInterface


def file_not_found_decorator(func):
    async def wrapper(*args, **kwargs):
        try:
            return await func(*args, **kwargs)
        except FileNotFoundError as e:
            raise FileNotFoundError(e)
    return wrapper


class LocalSaveImageLogic(SaveImageFileInterface):

    def __init__(self, path_to_save: str):
        self._path = path_to_save

    @staticmethod
    def generate_image_name(filename: str):
        return str(uuid4()) + ':' + filename

    @file_not_found_decorator
    async def read_image(self, filename: str):
        async with aiofiles.open(f'{self._path}/{filename}', mode='r') as f:
            image = await f.read()
            return image

    @file_not_found_decorator
    async def save_image(self, file: UploadFile, filename: str):
        async with aiofiles.open(f'{self._path}/{filename}', mode='wb') as f:
            content = await file.read()
            await f.write(content)

    @file_not_found_decorator
    async def delete_image(self, filename: str):
        await _os.remove(f'{self._path}/{filename}')
