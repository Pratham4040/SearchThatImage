"""SQLAlchemy model for an uploaded image and its AI-generated tags."""

from __future__ import annotations

from datetime import datetime, timezone

from app.models.database import db


class Image(db.Model):
    """Represents an uploaded image stored in the system.

    Attributes:
        id:         Primary key.
        filename:   Filename as stored on disk (UUID-based).
        original_filename: Original filename provided by the user.
        file_path:  Relative path inside the upload folder.
        tags:       Comma-separated AI-generated descriptive tags.
        created_at: UTC timestamp of upload.
    """

    __tablename__ = "images"

    id: int = db.Column(db.Integer, primary_key=True)
    filename: str = db.Column(db.String(255), nullable=False, unique=True)
    original_filename: str = db.Column(db.String(255), nullable=False)
    file_path: str = db.Column(db.String(512), nullable=False)
    tags: str = db.Column(db.Text, default="")
    created_at: datetime = db.Column(
        db.DateTime,
        nullable=False,
        default=lambda: datetime.now(timezone.utc),
    )

    def to_dict(self) -> dict[str, object]:
        """Serialise the model to a JSON-safe dictionary.

        Returns:
            Dictionary representation of the image record.
        """
        return {
            "id": self.id,
            "filename": self.filename,
            "original_filename": self.original_filename,
            "file_path": self.file_path,
            "tags": self.tags.split(",") if self.tags else [],
            "created_at": self.created_at.isoformat(),
        }
