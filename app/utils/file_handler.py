import os
from uuid import uuid4


UPLOAD_DIR = "app/uploads"


def save_uploaded_file(file):

    os.makedirs(UPLOAD_DIR, exist_ok=True)

    file_extension = file.filename.split(".")[-1]

    unique_filename = f"{uuid4()}.{file_extension}"

    file_path = os.path.join(UPLOAD_DIR, unique_filename)

    with open(file_path, "wb") as buffer:
        buffer.write(file.file.read())

    return file_path