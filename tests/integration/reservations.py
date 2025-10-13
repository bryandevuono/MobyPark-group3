import requests

BASE_URL = "http://localhost:8000"

# happy flow
def test_create_reservation():
    payload = {
        "username": "meneer6",
        "password": "secret"
    }

    # Register + login
    requests.post(f"{BASE_URL}/register", json=payload)
    response = requests.post(f"{BASE_URL}/login", json=payload)
    json_response = response.json()
    session_token = json_response["session_token"]
    print(session_token)

    headers = {
        "Authorization": session_token
    }

    # Create a reservation
    reservation_payload = {
        "parking_lot_id": 1,
        "vehicle_id": 1,
        "start_time": "2025-10-13T10:00:00",
        "end_time": "2025-10-13T12:00:00"
    }
    response = requests.post(f"{BASE_URL}/reservations", headers=headers, json=reservation_payload)
    assert response.status_code in [200, 201], f"Unexpected: {response.text}"


def test_get_reservations():
    payload = {
        "username": "meneer7",
        "password": "secret"
    }

    # Register + login
    requests.post(f"{BASE_URL}/register", json=payload)
    response = requests.post(f"{BASE_URL}/login", json=payload)
    json_response = response.json()
    session_token = json_response["session_token"]
    print(session_token)

    headers = {
        "Authorization": session_token
    }

    # Retrieve reservations
    response = requests.get(f"{BASE_URL}/reservations", headers=headers)
    assert response.status_code == 200


# sad flow
def test_create_reservation_invalid_parking_lot():
    payload = {
        "username": "meneer8",
        "password": "secret"
    }

    # Register + login
    requests.post(f"{BASE_URL}/register", json=payload)
    response = requests.post(f"{BASE_URL}/login", json=payload)
    json_response = response.json()
    session_token = json_response["session_token"]
    print(session_token)

    headers = {
        "Authorization": session_token
    }

    # Invalid reservation (non-existent parking lot)
    reservation_payload = {
        "parking_lot_id": 9999,
        "vehicle_id": 1,
        "start_time": "2025-10-13T10:00:00",
        "end_time": "2025-10-13T12:00:00"
    }
    response = requests.post(f"{BASE_URL}/reservations", headers=headers, json=reservation_payload)
    assert response.status_code in [400, 404], f"Unexpected: {response.status_code}, {response.text}"
