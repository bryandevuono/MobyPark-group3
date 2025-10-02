import requests

BASE_URL = "http://localhost:8000"


# happy flow
def test_create_user():
    payload = {
        "username": "johndoe",
        "email": "johndoe@example.com",
        "password": "strongpassword123",
        "name": "John Doe",
        "phone": "+1234567890",
        "birth_year": 1990,
    }
    response = requests.post(f"{BASE_URL}/register", json=payload)

    assert response.status_code == 200


def test_login():
    payload = {"username": "johndoe", "password": "strongpassword123"}
    response = requests.post(f"{BASE_URL}/login", json=payload)

    assert response.status_code == 200


# sad flow
def test_create_user_null_name():
    payload = {"username": "", "password": "secret"}
    response = requests.post(f"{BASE_URL}/register", json=payload)

    assert response.status_code != 200


def test_create_user_null_password():
    payload = {"username": "", "password": ""}
    response = requests.post(f"{BASE_URL}/register", json=payload)

    assert response.status_code != 200


def test_wrong_token():
    response = requests.get(f"{BASE_URL}/vehicles", headers={"Authorization": "Bearer dujshdsj"})

    assert response.status_code == 401


def test_duplicate_create_user():
    payload = {
        "username": "johndoe",
        "email": "johndoe@example.com",
        "password": "strongpassword123",
        "name": "John Doe",
        "phone": "+1234567890",
        "birth_year": 1990,
    }
    response = requests.post(f"{BASE_URL}/register", json=payload)

    assert response.status_code == 400
