"""SQLAlchemy model for tags and image-tag relationships."""

from __future__ import annotations

from typing import TYPE_CHECKING

from sqlalchemy.orm import Mapped

from app.models.database import db

if TYPE_CHECKING:
    from app.models.image import Image


# ── Many-to-Many Association Table ────────────────────────────────────────
# The image_tags table is a join table that links images to their tags.
# This allows:
#   - One image to have multiple tags
#   - One tag to be associated with multiple images
# We use a simple association table (not a full model) since we don't need
# extra data on the relationship itself (e.g. no timestamp on the join).
image_tags = db.Table(
    "image_tags",
    db.Column("image_id", db.Integer, db.ForeignKey("images.id", ondelete="CASCADE"), primary_key=True),
    db.Column("tag_id", db.Integer, db.ForeignKey("tags.id", ondelete="CASCADE"), primary_key=True),
)


class Tag(db.Model):
    """Represents an AI-generated descriptive tag.

    Attributes:
        id:     Primary key.
        name:   Unique, normalized tag name (lowercase, no duplicates).
        images: Relationship to Image models (bidirectional).
    """

    __tablename__ = "tags"

    id: Mapped[int] = db.mapped_column(db.Integer, primary_key=True)
    name: Mapped[str] = db.mapped_column(
        db.String(255),
        nullable=False,
        unique=True,
        index=True,
    )
    images: Mapped[list[Image]] = db.relationship(
        "Image",
        secondary=image_tags,
        back_populates="tag_objects",
        lazy="joined",
    )

    def to_dict(self) -> dict[str, object]:
        """Serialise the model to a JSON-safe dictionary.

        Returns:
            Dictionary representation of the tag record.
        """
        return {
            "id": self.id,
            "name": self.name,
            "image_count": len(self.images),
        }

    def __repr__(self) -> str:
        return f"<Tag {self.name!r}>"
