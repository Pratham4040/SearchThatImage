"""Entry point for the SearchThatImage Flask backend.

Run with:
    flask run          (development)
    gunicorn app:app   (production)
"""

from __future__ import annotations

import os
import sys

# Ensure the backend directory is in the Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app import create_app

app = create_app()

if __name__ == "__main__":
    debug_mode = os.getenv("FLASK_ENV") == "development"
    print(f"Starting Flask app in {'DEBUG' if debug_mode else 'PRODUCTION'} mode...")
    print(f"Database: {app.config['SQLALCHEMY_DATABASE_URI']}")
    print(f"Upload folder: {app.config['UPLOAD_FOLDER']}")
    print(f"CORS origins: {os.getenv('CORS_ORIGINS', 'http://localhost:5173')}")
    print("─" * 60)
    app.run(debug=debug_mode, host="127.0.0.1", port=5000)

