import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch
from datetime import datetime, timedelta, timezone

import app
from app.main import app
from app.utils.config import ACCESS_TOKEN_EXPIRE_MINUTES

client = TestClient(app)


@pytest.fixture
def fake_user():
    return {
        "id": "123",
        "name": "Test User",
        "email": "test@example.com"
    }


@pytest.fixture
def user_credentials():
    return {
        "name": "Test User",
        "email": "test@example.com",
        "password": "secret123"
    }


def get_token(user_id: str):
    from app.utils.security import gen_auth_token
    expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    return gen_auth_token(user_id, expire)


@patch("services.user.create_user")
@patch("utils.security.gen_auth_token")
def test_signup_success(mock_gen_token, mock_create_user, user_credentials, fake_user):
    mock_create_user.return_value = fake_user
    mock_gen_token.return_value = "test_token"

    response = client.post("/auth/signup", json=user_credentials)
    
    assert response.status_code == 201
    assert response.json()["email"] == fake_user["email"]
    assert "Authorization" in response.cookies


@patch("services.user.create_user")
def test_signup_when_already_logged_in(mock_create_user, user_credentials, fake_user):
    token = get_token(fake_user["id"])
    cookies = {"Authorization": token}

    response = client.post("/auth/signup", json=user_credentials, cookies=cookies)
    assert response.status_code == 400  # From AuthTokenProvidedException


@patch("services.user.authenticate_user")
@patch("utils.security.gen_auth_token")
def test_login_success(mock_gen_token, mock_auth_user, user_credentials, fake_user):
    mock_auth_user.return_value = fake_user
    mock_gen_token.return_value = "test_token"

    response = client.post("/auth/login", json=user_credentials)

    assert response.status_code == 200
    assert response.json()["email"] == fake_user["email"]
    assert "Authorization" in response.cookies


def test_login_when_already_logged_in(fake_user):
    token = get_token(fake_user["id"])
    cookies = {"Authorization": token}

    response = client.post("/auth/login", json={
        "email": fake_user["email"],
        "password": "any"
    }, cookies=cookies)

    assert response.status_code == 400  # From AuthTokenProvidedException


def test_is_logged_in_true(fake_user):
    token = get_token(fake_user["id"])
    cookies = {"Authorization": token}

    response = client.get("/auth/login", cookies=cookies)

    assert response.status_code == 200
    assert response.json() == {"is_logged_in": True}


def test_is_logged_in_false():
    response = client.get("/auth/login")
    assert response.status_code == 200
    assert response.json() == {"is_logged_in": False}


def test_logout():
    cookies = {"Authorization": "anytoken"}
    response = client.post("/auth/logout", cookies=cookies)

    assert response.status_code == 200
    assert response.json() == {"message": "Logged out"}
