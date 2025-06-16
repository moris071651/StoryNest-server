import pytest
from datetime import datetime, timedelta, timezone
from uuid import uuid4
from jose import jwt

from app.utils.sec import (
    valid_expire_date,
    gen_auth_token,
    verify_auth_token,
    get_auth_data,
    get_auth_user,
)

@pytest.fixture
def user_id():
    return uuid4()


@pytest.fixture
def expire_date():
    return datetime.now(timezone.utc) + timedelta(minutes=10)


def test_valid_expire_date_with_valid_datetime(expire_date):
    assert valid_expire_date(expire_date) == True


def test_valid_expire_date_with_expired_datetime():
    past_date = datetime.now(timezone.utc) - timedelta(minutes=10)
    assert valid_expire_date(past_date) == False


def test_valid_expire_date_with_iso_string(expire_date):
    iso = expire_date.isoformat()
    assert valid_expire_date(iso) == True


def test_valid_expire_date_with_invalid_type():
    assert valid_expire_date(12345) == False


def test_gen_auth_token_returns_jwt(user_id, expire_date):
    token = gen_auth_token(user_id, expire_date)
    payload = jwt.decode(token, "JWT_SECRET", algorithms="HS256")
    assert payload["user_id"] == str(user_id)
    assert payload["expire"] == expire_date.isoformat()


def test_verify_auth_token_valid(mock_verify_user_id, user_id, expire_date):
    token = gen_auth_token(user_id, expire_date)
    assert verify_auth_token(token) == True


def test_verify_auth_token_invalid_user(mock_verify_user_id, user_id, expire_date):
    token = gen_auth_token(user_id, expire_date)
    assert verify_auth_token(token) == False


def test_verify_auth_token_expired(mock_verify_user_id, user_id):
    expired = datetime.now(timezone.utc) - timedelta(minutes=5)
    token = gen_auth_token(user_id, expired)
    assert verify_auth_token(token) == False


def test_get_auth_data(user_id, expire_date):
    token = gen_auth_token(user_id, expire_date)
    data = get_auth_data(token)
    assert data["user_id"] == str(user_id)


def test_get_auth_user_valid(mock_verify_user_id, user_id, expire_date):
    token = gen_auth_token(user_id, expire_date)
    result = get_auth_user(token)
    assert result == user_id
    

def test_get_auth_user_invalid_user(mock_verify_user_id, user_id, expire_date):
    token = gen_auth_token(user_id, expire_date)
    assert get_auth_user(token) is None


def test_get_auth_user_none():
    assert get_auth_user(None) is None
