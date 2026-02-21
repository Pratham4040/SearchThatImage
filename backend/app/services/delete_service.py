"""Service for deleting images and their files."""

from __future__ import annotations

import logging
from pathlib import Path

from app.models.database import db
from app.models.image import Image

logger = logging.getLogger(__name__)


def delete_image_record(image_id: int, upload_folder: str) -> bool:
    """Delete an image record and its file from disk.

    Args:
        image_id: Primary key of the image record.
        upload_folder: Absolute path to the uploads directory.

    Returns:
        True if deleted, False if not found.
    """
    image = db.session.get(Image, image_id)
    if image is None:
        return False

    file_path = Path(image.file_path)
    if not file_path.is_absolute():
        file_path = Path(upload_folder) / file_path.name

    if file_path.exists():
        try:
            file_path.unlink()
        except OSError:
            logger.warning("Failed to delete file from disk: %s", file_path)

    db.session.delete(image)
    db.session.commit()
    logger.info("Deleted image: %s", image.filename)
    return True
