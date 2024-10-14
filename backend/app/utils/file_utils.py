import os
import uuid

from app.models.file import File


def save_uploaded_file(file, filename):
    try:
        os.mkdir("uploads")
    except FileExistsError:
        pass
    with open(filename, "wb") as f:
        f.write(file.file.read())
        f.close()
    return True


def upload_file_s3(file, path):
    pass


def download_file_s3(file, path):
    pass


def is_valid_file(filename) -> bool:
    file = File(name=filename)
    if file.type is None:
        return False
    return True


def get_file_type(filename):
    file = File(name=filename)
    return file.type


def file_uuid():
    return str(uuid.uuid4())
