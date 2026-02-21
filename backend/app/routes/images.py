"""Blueprint for image upload and retrieval endpoints."""

from __future__ import annotations

from pathlib import Path

from flask import Blueprint, current_app, jsonify, request, send_file, send_from_directory

from app.services.image_service import get_all_images, get_image_by_id, save_image

images_bp = Blueprint("images", __name__)


@images_bp.route("/", methods=["GET"])
def list_images() -> tuple:
    """Return a paginated list of all uploaded images.

    Query params:
        page  (int, default 1):      Page number.
        limit (int, default 20):     Results per page.

    Returns:
        JSON array of image objects.
    """
    page: int = int(request.args.get("page", 1))
    limit: int = min(int(request.args.get("limit", 20)), 100)
    all_images = get_all_images()
    start: int = (page - 1) * limit
    paginated = all_images[start : start + limit]
    return jsonify(
        {
            "images": [img.to_dict() for img in paginated],
            "total": len(all_images),
            "page": page,
            "limit": limit,
        }
    ), 200


@images_bp.route("/<int:image_id>", methods=["GET"])
def get_image(image_id: int) -> tuple:
    """Return details for a single image by ID.

    Args:
        image_id: Primary key of the image record.

    Returns:
        JSON object with image details or 404 error.
    """
    image = get_image_by_id(image_id)
    if image is None:
        return jsonify({"error": "Image not found", "status": 404}), 404
    return jsonify(image.to_dict()), 200


@images_bp.route("/upload", methods=["POST"])
def upload_image() -> tuple:
    """Accept a multipart file upload, tag it with AI, and persist it.

    Form data:
        image (file): The image file to upload.

    Returns:
        JSON object of the created image record (201) or an error response.
    """
    if "image" not in request.files:
        return jsonify({"error": "No image field in request", "status": 400}), 400

    file = request.files["image"]
    if not file.filename:
        return jsonify({"error": "No file selected", "status": 400}), 400

    try:
        image = save_image(file, current_app.config["UPLOAD_FOLDER"])
        return jsonify(image.to_dict()), 201
    except ValueError as exc:
        return jsonify({"error": str(exc), "status": 400}), 400
    except TimeoutError as exc:
        return jsonify({"error": f"AI processing timed out: {str(exc)}", "status": 504}), 504
    except Exception as exc:
        # Catch any other unexpected errors
        return jsonify({"error": f"Server error: {str(exc)}", "status": 500}), 500


@images_bp.route("/file/<path:filename>", methods=["GET"])
def serve_image(filename: str) -> object:
    """Serve an uploaded image file directly.

    Args:
        filename: The stored filename (UUID-based) to retrieve.

    Returns:
        The binary image file or a 404 error.
    """
    safe_name = Path(filename).name
    upload_root = Path(current_app.config["UPLOAD_FOLDER"])
    candidate = upload_root / safe_name
    if candidate.exists():
        return send_file(candidate)

    # Fallback for legacy paths if config mismatches
    backend_root = Path(__file__).resolve().parent.parent.parent
    legacy_candidate = backend_root / "uploads" / safe_name
    if legacy_candidate.exists():
        return send_file(legacy_candidate)

    return jsonify({"error": "Image file not found", "status": 404}), 404
