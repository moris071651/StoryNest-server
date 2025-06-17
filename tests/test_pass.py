import pytest
from app.utils.password import hash_password, verify_password


def test_hash_password_is_not_plaintext():
    password = "supersecret"
    hashed = hash_password(password)
    assert hashed != password
    assert isinstance(hashed, str)
    assert hashed.startswith("$2b$") or hashed.startswith("$2a$")


def test_verify_password_success():
    password = "mypassword"
    hashed = hash_password(password)
    assert verify_password(password, hashed) == True


def test_verify_password_failure():
    password = "mypassword"
    wrong_password = "wrongpass"
    hashed = hash_password(password)
    assert verify_password(wrong_password, hashed) == False


def test_verify_with_invalid_hash_fails():
    password = "test"
    with pytest.raises(ValueError):
        verify_password(password, "not_a_valid_hash")


def test_hash_password_is_not_plaintext2():
    password = "supersecretijuiusuiu"
    hashed = hash_password(password)
    assert hashed != password
    assert isinstance(hashed, str)
    assert hashed.startswith("$2b$") or hashed.startswith("$2a$")


def test_verify_password_success2():
    password = "mypasswordijuiusuiu"
    hashed = hash_password(password)
    assert verify_password(password, hashed) == True


def test_verify_password_failure2():
    password = "mypasswordijuiusuiu"
    wrong_password = "wrongpassijuiusuiu"
    hashed = hash_password(password)
    assert verify_password(wrong_password, hashed) == False


def test_verify_with_invalid_hash_fails2():
    password = "testijuiusuiu"
    with pytest.raises(ValueError):
        verify_password(password, "noijuiusuiut_a_valid_hash")
