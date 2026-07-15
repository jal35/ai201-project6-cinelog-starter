"""
tests/test_watchlist.py — CineLog (feature/watchlist branch)

Tests for the watchlist service.
Modeled on test_add_to_collection_nonexistent_film_raises in test_collection.py.
"""

import pytest
from app import create_app, db
from services.watchlist_service import add_to_watchlist
from services.collection_service import FilmNotFoundError


@pytest.fixture
def db_session():
    """Provide an isolated in-memory database session for each test."""
    app = create_app(config={
        "TESTING": True,
        "SQLALCHEMY_DATABASE_URI": "sqlite:///:memory:",
    })
    with app.app_context():
        db.create_all()
        yield db.session
        db.session.remove()
        db.drop_all()


# ── Nonexistent film ─────────────────────────────────────────────────────────

def test_add_to_watchlist_nonexistent_film_raises(db_session):
    """
    Adding a film_id that doesn't exist in the database should raise
    FilmNotFoundError, not a database integrity error.
    """
    with pytest.raises(FilmNotFoundError):
        add_to_watchlist(user_id="some-user-uuid", film_id=999)
