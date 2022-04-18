import aiofiles
from aiofiles import os as _os
from fastapi import UploadFile

from .interfaces.image_service_interface import SaveImageFileInterface


class LocalSaveImageService(SaveImageFileInterface):

    def __init__(self, path_to_save: str):
        self._path = path_to_save

    async def read_image(self, filename: str):
        try:
            async with aiofiles.open(f'{self._path}/{filename}', mode='r') as f:
                image = await f.read()
            return image
        except FileNotFoundError as e:
            raise FileNotFoundError(e)

    async def save_image(self, file: UploadFile, filename: str):
        async with aiofiles.open(f'{self._path}/{filename}', mode='wb') as f:
            content = await file.read()
            await f.write(content)

    async def delete_image(self, filename: str):
        try:
            await _os.remove(f'{self._path}/{filename}')
        except FileNotFoundError as e:
            raise FileNotFoundError(e)
