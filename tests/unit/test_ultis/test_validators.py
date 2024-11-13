# tests/unit/test_utils/test_validators.py
import pytest
from app.utils.validators import validate_email

def test_valid_email():
    assert validate_email('test@example.com') is True

def test_invalid_email():
    assert validate_email('invalid-email') is False
