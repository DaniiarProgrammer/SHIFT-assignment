#tests\test_auth.py:

from app.auth import hash_password, verify_password

def test_hash_password_returns_bcrypt_hash():
    result = hash_password("testpassword")
    assert result.startswith("$2b$")
    assert len(result) == 60

def test_hash_password_different_each_time():
    first_result = hash_password("same")
    second_result = hash_password("same")
    assert first_result != second_result

def test_verify_password_correct():
    hashed = hash_password("testpassword")
    assert verify_password("testpassword", hashed) == True

def test_verify_password_wrong():
    hashed = hash_password("testpassword")
    assert verify_password("wrongpassword", hashed) == False