"""SQLAlchemy model for an uploaded image and its AI-generated tags."""

from __future__ import annotations

from datetime import datetime, timezone
from typing import TYPE_CHECKING

from sqlalchemy.orm import Mapped

from app.models.database import db

if TYPE_CHECKING:
    from app.models.tag import Tag


class Image(db.Model):
    """Represents an uploaded image stored in the system.

    Attributes:
        id:                 Primary key.
        filename:           Filename as stored on disk (UUID-based).
        original_filename:  Original filename provided by the user.
        file_path:          Relative path inside the upload folder.
        tags:               Comma-separated AI-generated descriptive tags (legacy).
        tag_objects:        Relationship to Tag models (bidirectional).
        created_at:         UTC timestamp of upload.
    """

    __tablename__ = "images"

    id: Mapped[int] = db.mapped_column(db.Integer, primary_key=True)
    filename: Mapped[str] = db.mapped_column(db.String(255), nullable=False, unique=True)
    original_filename: Mapped[str] = db.mapped_column(db.String(255), nullable=False)
    file_path: Mapped[str] = db.mapped_column(db.String(512), nullable=False)
    tags: Mapped[str] = db.mapped_column(db.Text, default="")
    tag_objects: Mapped[list[Tag]] = db.relationship(
        "Tag",
        secondary="image_tags",
        back_populates="images",
        cascade="all, delete",
        lazy="joined",
    )
    created_at: Mapped[datetime] = db.mapped_column(
        db.DateTime,
        nullable=False,
        default=lambda: datetime.now(timezone.utc),
    )

    def to_dict(self) -> dict[str, object]:
        """Serialise the model to a JSON-safe dictionary.

        Returns:
            Dictionary representation of the image record.
        """
        tag_objects = self.tag_objects or []
        return {
            "id": self.id,
            "filename": self.filename,
            "original_filename": self.original_filename,
            "file_path": self.file_path,
            "tags": [tag for tag in (self.tags.split(",") if self.tags else []) if tag],
            "tag_names": [tag.name for tag in tag_objects if tag and tag.name],
            "created_at": self.created_at.isoformat() if self.created_at else None,
        }
