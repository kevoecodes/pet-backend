import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent


class ConstantsProvider:
    # MEDIA_FOLDER_PATH = '/mnt/volume_ams3_01/SMART_MAUZO_RES/media/'
    MEDIA_FOLDER_PATH = f'{BASE_DIR.parent.parent}/media'

    @staticmethod
    def get_image_path():
        path = os.path.join(ConstantsProvider.MEDIA_FOLDER_PATH, 'images')
        if not os.path.exists(path):
            os.makedirs(path)
        return path

    @staticmethod
    def get_files_path():
        path = os.path.join(ConstantsProvider.MEDIA_FOLDER_PATH, 'files')
        if not os.path.exists(path):
            os.makedirs(path)
        return path


class Constant:
    image_path = ConstantsProvider.get_image_path()
    files_path = ConstantsProvider.get_files_path()
