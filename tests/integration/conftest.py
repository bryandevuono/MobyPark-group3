# conftest.py
import pytest
import requests

BASE_URL = "http://localhost:8000"

@pytest.fixture(scope="session")
def headers():
    register_payload = {
        "username": "johndoe",
        "email": "johndoe@example.com",
        "password": "strongpassword123",
        "name": "John Doe",
        "phone": "+1234567890",
        "birth_year": 1990,
        "role": "admin"
    }
    try:
        requests.post(f"{BASE_URL}/register", json=register_payload)
    except requests.exceptions.RequestException:
        pass

    login_payload = {
        "username": "johndoe",
        "password": "strongpassword123"
    }
    response = requests.post(f"{BASE_URL}/login", json=login_payload)
    response.raise_for_status()
    token = response.json().get("access_token")

    return {"Authorization": f"Bearer {token}"}
