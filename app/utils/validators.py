from app.core.exceptions import ValidationException


ALLOWED_EXTENSIONS = [
    "png",
    "jpg",
    "jpeg"
]


def validate_file_extension(filename: str):

    extension = filename.split(".")[-1].lower()

    if extension not in ALLOWED_EXTENSIONS:

        raise ValidationException(
            f"Unsupported file type: {extension}"
        )
