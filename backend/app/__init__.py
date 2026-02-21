"""Application factory for SearchThatImage Flask backend."""

from __future__ import annotations

import os
from pathlib import Path

from dotenv import load_dotenv
from flask import Flask
from flask_cors import CORS

from app.models.database import db

load_dotenv()


def create_app() -> Flask:
    """Create and configure the Flask application.

    Returns:
        Configured Flask application instance.
    """
    app = Flask(__name__, instance_relative_config=False)

    # ── Configuration ─────────────────────────────────────────────────────────
    app.config["SECRET_KEY"] = os.getenv("SECRET_KEY", "dev-secret-change-me")
    app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv(
        "DATABASE_URL", "sqlite:///searchthatimage.db"
    )
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    upload_folder = Path(os.getenv("UPLOAD_FOLDER", "uploads"))
    if not upload_folder.is_absolute():
        # Resolve relative upload paths against the backend root directory.
        backend_root = Path(__file__).resolve().parent.parent
        upload_folder = backend_root / upload_folder
    upload_folder.mkdir(parents=True, exist_ok=True)
    app.config["UPLOAD_FOLDER"] = str(upload_folder)
    app.config["MAX_CONTENT_LENGTH"] = (
        int(os.getenv("MAX_CONTENT_LENGTH_MB", "16")) * 1024 * 1024
    )

    # ── Extensions ────────────────────────────────────────────────────────────
    db.init_app(app)
    CORS(app, origins=os.getenv("CORS_ORIGINS", "http://localhost:5173").split(","))

    # ── Blueprints ────────────────────────────────────────────────────────────
    from app.routes.images import images_bp
    from app.routes.search import search_bp

    app.register_blueprint(images_bp, url_prefix="/api/images")
    app.register_blueprint(search_bp, url_prefix="/api/search")

    # ── Health check endpoint ─────────────────────────────────────────────────
    @app.route("/api/health", methods=["GET"])
    def health_check():
        """Simple health check endpoint to verify backend is running."""
        return {"status": "ok", "message": "Backend is running"}, 200

    # ── Database initialisation ───────────────────────────────────────────────
    with app.app_context():
        # Import models BEFORE create_all() so SQLAlchemy knows about them
        from app.models.image import Image  # noqa: F401
        from app.models.tag import Tag  # noqa: F401

        db.create_all()

    return app
