"""Search service – business logic for querying images by tags."""

from __future__ import annotations

from app.models.database import db
from app.models.image import Image


def search_images_by_tags(query: str) -> list[Image]:
    """Search for images whose stored tags contain the given query string.

    The search is case-insensitive and matches any tag that contains the
    query as a substring (e.g. "cat" matches "black-cat" and "catfish").

    Args:
        query: Search term provided by the user.

    Returns:
        List of matching Image ORM objects ordered by most recent first.
    """
    if not query or not query.strip():
        return []

    normalised: str = query.strip().lower()

    results = (
        db.session.execute(
            db.select(Image)
            .where(Image.tags.ilike(f"%{normalised}%"))
            .order_by(Image.created_at.desc())
        )
        .scalars()
        .all()
    )
    return results
