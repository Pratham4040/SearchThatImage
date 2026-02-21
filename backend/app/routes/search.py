"""Blueprint for image search endpoints."""

from __future__ import annotations

from flask import Blueprint, jsonify, request

from app.services.search_service import search_images_by_tags

search_bp = Blueprint("search", __name__)


@search_bp.route("/", methods=["GET"])
def search() -> tuple:
    """Search images by tag keywords.

    Query params:
        q (str): The search query string.

    Returns:
        JSON array of matching image objects or a 400 error if query is empty.
    """
    query: str = request.args.get("q", "").strip()
    if not query:
        return jsonify({"error": "Query parameter 'q' is required", "status": 400}), 400

    results = search_images_by_tags(query)
    return jsonify(
        {
            "query": query,
            "results": [img.to_dict() for img in results],
            "count": len(results),
        }
    ), 200
