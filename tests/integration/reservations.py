import requests
import pytest

BASE_URL = "http://localhost:8000"

@pytest.fixture(scope="session")
def headers():
    """Register a test user and return auth headers with token."""
    payload = {
        "username": "reservation_user",
        "email": "reservation_user@example.com",
        "password": "secret123",
        "name": "Reservation Tester",
        "phone": "+1234567890",
        "birth_year": 1995
    }
    requests.post(f"{BASE_URL}/register", json=payload)

    # Login
    login_payload = {"username": "reservation_user", "password": "secret123"}
    response = requests.post(f"{BASE_URL}/login", json=login_payload)
    response.raise_for_status()

    json_response = response.json()
    token = json_response.get("access_token") or json_response.get("session_token")

    return {"Authorization": f"Bearer {token}"}


# happy flow
def test_create_reservation(headers):
    reservation_payload = {
        "parking_lot_id": 1,
        "vehicle_id": 1,
        "start_time": "2025-10-13T10:00:00",
        "end_time": "2025-10-13T12:00:00"
    }

    response = requests.post(f"{BASE_URL}/reservations", headers=headers, json=reservation_payload)
    assert response.status_code in [200, 201], f"Unexpected: {response.status_code}, {response.text}"
    data = response.json()
    assert "id" in data, "Reservation ID not returned"

def test_get_reservations(headers):
    response = requests.get(f"{BASE_URL}/reservations", headers=headers)
    assert response.status_code == 200
    assert isinstance(response.json(), list)


# sad flow
def test_create_reservation_invalid_parking_lot(headers):
    invalid_payload = {
        "parking_lot_id": 676767,
        "vehicle_id": 1,
        "start_time": "2025-10-13T10:00:00",
        "end_time": "2025-10-13T12:00:00"
    }

    response = requests.post(f"{BASE_URL}/reservations", headers=headers, json=invalid_payload)
    assert response.status_code in [400, 404], f"Unexpected: {response.status_code}, {response.text}"
