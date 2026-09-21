import pytest
from sqlalchemy import text
from app.db.session import get_db


def test_db_session_lifecycle():
    generator = get_db()
    session = next(generator)
    try:
        assert session.is_active
        result = session.execute(text("SELECT 1 AS alive")).fetchone()
        assert result[0] == 1
    finally:
        try:
            next(generator)
        except StopIteration:
            pass


def test_db_session_rollback_on_error(db_session):
    # Test that rollback handles invalid statements gracefully
    with pytest.raises(Exception):
        db_session.execute(text("SELECT * FROM non_existent_table_for_testing"))
    db_session.rollback()
    # Verify session is still usable after rollback
    result = db_session.execute(text("SELECT 42 AS test")).fetchone()
    assert result[0] == 42
