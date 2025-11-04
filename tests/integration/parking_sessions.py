import requests

BASE_URL = "http://localhost:8000"

# happy flow
def test_get_all_sessions(headers: dict) -> None:
    response = requests.get(f"{BASE_URL}/parking-lots/1/sessions", headers=headers)
    assert response.status_code == 200
    
def test__get_parking_session(headers: dict) -> None:
    response = requests.get(f"{BASE_URL}/parking-lots/1/sessions/1", headers=headers)
    assert response.status_code == 200


def test__start_parking_session(headers: dict) -> None:
    payload = {
        "name": "Central Park Garage",
        "location": "Downtown",
        "address": "123 Main Street, Cityville",
        "capacity": 150,
        "reserved": 20,
        "tariff": 2.5,
        "daytariff": 20.0,
        "latitude": 40.785091,
        "longitude": -73.968285,
    }
    requests.post(f"{BASE_URL}/parking-lots", headers=headers, json=payload)
    
    payload = {
        "license_plate": "AAC123",
        "make": "Toyoata",
        "model": "Codrolla",
        "color": "Red",
        "year": 2020
    }
    requests.post(f"{BASE_URL}/vehicles", headers=headers, json=payload)
    
    payload = {
        "parking_lots_id": 1,
        "vehicles_id": 1
    }
    response = requests.post(f"{BASE_URL}/parking-lots/1/sessions/start", headers=headers, json=payload)
    assert response.status_code == 200

def test_delete_session(headers:dict) -> None:
    response = requests.delete(f"{BASE_URL}/parking-lots/1/sessions/1", headers=headers)
    assert response.status_code == 200
    
# sad flow
def test_start_non_existing_parking_lot(headers: dict) -> None:
    payload = {
        "parking_lots_id": 9999,
        "vehicles_id": 9999
    }
    response = requests.post(f"{BASE_URL}/parking-lots/-9999/sessions/start", headers=headers, json=payload)
    assert response.status_code == 404
    
def test_delete_non_existing_session(headers: dict) -> None:
    response = requests.delete(f"{BASE_URL}/parking-lots/1/sessions/9999", headers=headers)
    assert response.status_code >= 400

def test_update_non_existing_session(headers: dict) -> None:
    payload = {
        "parking_lots_id": 9999,
        "vehicles_id": 9999
    }
    response = requests.put(f"{BASE_URL}/parking-lots/-9999/sessions/1", headers=headers, json=payload)
    assert response.status_code == 405

def test_stop_non_existing_session(headers: dict) -> None:
    payload = {
        "parking_lots_id": 9999,
        "vehicles_id": 9999
    }
    response = requests.post(f"{BASE_URL}/parking-lots/-9999/sessions/stop", headers=headers, json=payload)
    assert response.status_code == 405
    
    