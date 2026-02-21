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

    # ── Database initialisation ───────────────────────────────────────────────
    with app.app_context():
        db.create_all()

    return app
