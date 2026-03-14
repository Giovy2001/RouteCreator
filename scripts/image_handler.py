import os


def init_image(upload_path: str):
    if not os.path.isdir(upload_path):
        os.makedirs(upload_path)