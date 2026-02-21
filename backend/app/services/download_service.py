"""Service for resolving image downloads."""

from __future__ import annotations

from pathlib import Path

from app.models.database import db
from app.models.image import Image


def get_image_download(image_id: int, upload_folder: str) -> tuple[Path, str] | None:
    """Resolve the file path for an image download.

    Args:
        image_id: Primary key of the image record.
        upload_folder: Absolute path to the uploads directory.

    Returns:
        Tuple of (file_path, original_filename) or None if not found.
    """
    image = db.session.get(Image, image_id)
    if image is None:
        return None

    file_path = Path(image.file_path)
    if not file_path.is_absolute():
        file_path = Path(upload_folder) / file_path.name

    if not file_path.exists():
        return None

    return file_path, image.original_filename
