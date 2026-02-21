"""Database initialisation and shared SQLAlchemy instance."""

from flask_sqlalchemy import SQLAlchemy

db: SQLAlchemy = SQLAlchemy()
