"""Image service – business logic for uploading and managing images."""

from __future__ import annotations

import os
import uuid
from pathlib import Path

from werkzeug.datastructures import FileStorage
from werkzeug.utils import secure_filename

from app.models.database import db
from app.models.image import Image
from app.services.ai_service import get_image_tags

ALLOWED_EXTENSIONS: set[str] = {
    ext.strip()
    for ext in os.getenv("ALLOWED_EXTENSIONS", "png,jpg,jpeg,gif,webp").split(",")
}


def _allowed_file(filename: str) -> bool:
    """Check whether the file extension is in the allow-list.

    Args:
        filename: Original filename provided by the client.

    Returns:
        True if the extension is permitted, False otherwise.
    """
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


def save_image(file: FileStorage, upload_folder: str) -> Image:
    """Validate, save, and tag an uploaded image file.

    Args:
        file:          The uploaded file object from Flask's request.
        upload_folder: Absolute path to the directory where files are stored.

    Returns:
        Newly created and committed Image database record.

    Raises:
        ValueError: If the file type is not allowed.
        RuntimeError: If the AI tag extraction fails.
    """
    original_filename: str = secure_filename(file.filename or "upload")

    if not _allowed_file(original_filename):
        raise ValueError(
            f"File type not allowed. Permitted types: {', '.join(ALLOWED_EXTENSIONS)}"
        )

    ext: str = original_filename.rsplit(".", 1)[1].lower()
    unique_filename: str = f"{uuid.uuid4().hex}.{ext}"
    file_path: Path = Path(upload_folder) / unique_filename

    file.save(str(file_path))

    tags: list[str] = get_image_tags(file_path)

    image = Image(
        filename=unique_filename,
        original_filename=original_filename,
        file_path=str(file_path),
        tags=",".join(tags),
    )
    db.session.add(image)
    db.session.commit()

    return image


def get_all_images() -> list[Image]:
    """Retrieve all image records ordered by most recent first.

    Returns:
        List of Image ORM objects.
    """
    return db.session.execute(
        db.select(Image).order_by(Image.created_at.desc())
    ).scalars().all()


def get_image_by_id(image_id: int) -> Image | None:
    """Fetch a single image record by primary key.

    Args:
        image_id: Primary key of the image record.

    Returns:
        Image ORM object or None if not found.
    """
    return db.session.get(Image, image_id)
