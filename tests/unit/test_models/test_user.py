# tests/unit/test_models/test_user.py
import pytest
from app.models import User

def test_password_hashing(init_db):
    user = User.query.first()
    assert user.check_password('testpassword') is True
    assert user.check_password('wrongpassword') is False
