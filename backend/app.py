"""Entry point for the SearchThatImage Flask backend.

Run with:
    flask run          (development)
    gunicorn app:app   (production)
"""

from __future__ import annotations

import os

from app import create_app

app = create_app()

if __name__ == "__main__":
    app.run(debug=os.getenv("FLASK_ENV") == "development")
