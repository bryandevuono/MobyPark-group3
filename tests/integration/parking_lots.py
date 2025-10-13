import requests

BASE_URL = "http://localhost:8000"

# happy flow
def test___get_all_parking_lots(headers):
    response = requests.get(f"{BASE_URL}/parking-lots", headers=headers)
    assert response.status_code == 200

def test_z_get_parking_lot(headers):
    response = requests.get(f"{BASE_URL}/parking-lots/1", headers=headers)
    assert response.status_code == 200

def test__add_parking_lot(headers):
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
    response = requests.post(f"{BASE_URL}/parking-lots", headers=headers, json=payload)
    assert response.status_code in [200, 201], f"Unexpected response: {response.status_code}, {response.text}"

def test_update_parking_lot(headers):
    payload = {
        "name": "Central Park Garage updated",
        "location": "Downtown",
        "address": "123 Main Street, Cityville",
        "capacity": 150,
        "reserved": 20,
        "tariff": 2.5,
        "daytariff": 20.0,
        "latitude": 40.785091,
        "longitude": -73.968285,
    }
    response = requests.put(f"{BASE_URL}/parking-lots/1", headers=headers, json=payload)
    assert response.status_code in [200, 201], f"Unexpected response: {response.status_code}"

def delete_parking_lot(headers):
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
    response = requests.post(f"{BASE_URL}/parking-lots", headers=headers, json=payload)
    parking_lot_id = response.json()["id"]

    response =  requests.delete(f"{BASE_URL}/parking-lots/{parking_lot_id}", headers=headers)
    assert response.status_code == 200

    response = requests.get(f"{BASE_URL}/parking-lots/{parking_lot_id}", headers=headers)
    assert response.status_code == 200

# sad flow
def test_get_parking_lot_non_existing(headers):
    response = requests.get(f"{BASE_URL}/parking-lots/9999", headers=headers)
    assert response.status_code == 404

def test_add_parking_lot_empty_required_field(headers):
    payload = {
        "name": "",
        "location": "Downtown",
        "address": "123 Main Street, Cityville",
        "capacity": 150,
        "reserved": 20,
        "tariff": 2.5,
        "daytariff": 20.0,
        "latitude": 40.785091,
        "longitude": -73.968285,
    }
    response = requests.post(f"{BASE_URL}/parking-lots", headers=headers, json=payload)
    assert response.status_code >= 400

def test_update_parking_lot_validation(headers):
    payload = {
        "name": "Central Park Garage updated",
        "location": "Downtown",
        "address": "123 Main Street, Cityville",
        "capacity": -1,
        "reserved": 20,
        "tariff": 2.5,
        "daytariff": 20.0,
        "latitude": 40.785091,
        "longitude": -73.968285,
    }
    response = requests.put(f"{BASE_URL}/parking-lots/1", headers=headers, json=payload)
    assert response.status_code >= 400

def test_delete_non_existing(headers):
    response =  requests.delete(f"{BASE_URL}/parking-lots/9999", headers=headers)
    assert response.status_code != 200