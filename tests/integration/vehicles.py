import requests
import pytest

BASE_URL = "http://localhost:8000"

@pytest.fixture(scope="session")
def headers():
    payload = {
        "username": "johndoe",
        "email": "johndoe@example.com",
        "password": "strongpassword123",
        "name": "John Doe",
        "phone": "+1234567890",
        "birth_year": 1990
    }
    requests.post(f"{BASE_URL}/register", json=payload)
    
    payload = {
        "username": "johndoe",
        "password": "strongpassword123"
    }
    response = requests.post(f"{BASE_URL}/login", json=payload)
    response.raise_for_status()
    token = response.json()["access_token"]
    
    return {"Authorization": f"Bearer {token}"}

def test___get_all_vehicles(headers):
    response = requests.get(f"{BASE_URL}/vehicles", headers=headers)
    assert response.status_code == 200

def test_add_vehicle(headers):
    payload = {
        "license_plate": "AAC123",
        "make": "Toyoata",
        "model": "Codrolla",
        "color": "Red",
        "year": 2020
    }
    response = requests.post(f"{BASE_URL}/vehicles", headers=headers, json=payload)
    assert response.status_code in [200, 201], f"Unexpected response: {response.status_code}, {response.text}"

def test_get_vehicle(headers):
    payload = {
        "license_plate": "BCC111",
        "make": "Honda",
        "model": "Civic",
        "color": "Blue",
        "year": 2021
    }
    
    response = requests.post(f"{BASE_URL}/vehicles", headers=headers, json=payload)
    response_json = response.json()
    vehicle_id = response_json["id"]
    
    response = requests.get(f"{BASE_URL}/vehicles/{vehicle_id}", headers=headers)
    assert response.status_code == 200

def test_update_vehicle(headers):
    payload = {
        "license_plate": "ASAB333",
        "make": "Ford",
        "model": "Focus",
        "color": "Black",
        "year": 2019
    }
    response = requests.post(f"{BASE_URL}/vehicles", headers=headers, json=payload)
    json_response = response.json()
    vehicle_id = json_response["id"]
    
    payload = {
        "license_plate": "ASAA000",
        "make": "Ford",
        "model": "Fiesta",
        "color": "Green",
        "year": 2020
    }
    response = requests.put(f"{BASE_URL}/vehicles/{vehicle_id}", headers=headers, json=payload)
    assert response.status_code == 200

def test_deleting_vehicle(headers): 
    payload = {
        "license_plate": "SSAAA",
        "make": "Nissan",
        "model": "Altima",
        "color": "White",
        "year": 2021
    }
    response = requests.post(f"{BASE_URL}/vehicles", headers=headers, json=payload)
    vehicle_id = response.json()["id"]
    
    response = requests.delete(f"{BASE_URL}/vehicles/{vehicle_id}", headers=headers)
    assert response.status_code == 200

def test_get_vehicles_no_auth():
    payload = {"username": "", "password": ""}
    response = requests.post(f"{BASE_URL}/login", json=payload)
    json_response = response.json()
    access_token = json_response.get("access_token", "")
    headers = {"Authorization": f"Bearer {access_token}"}
    response = requests.get(f"{BASE_URL}/vehicles", headers=headers)
    assert response.status_code != 200

def delete_non_existing_vehicle(headers):
    response = requests.delete(f"{BASE_URL}/vehicles/1000", headers=headers)
    assert response.status_code == 404

def test__get_non_existing_vehicle(headers):
    response = requests.get(f"{BASE_URL}/vehicles/1111", headers=headers)
    assert response.status_code == 200

def test_update_non_existing_vehicle(headers):
    payload = {
        "license_plate": "NON123",
        "make": "Honda",
        "model": "Civic",
        "color": "Yellow",
        "year": 2021
    }
    response = requests.put(f"{BASE_URL}/vehicles/111", headers=headers, json=payload)
    assert response.status_code == 404

def test_update_empty_string(headers):
    payload = {
        "license_plate": "",
        "make": "",
        "model": "",
        "color": "",
        "year": 0
    }
    response = requests.put(f"{BASE_URL}/vehicles/111", headers=headers, json=payload)
    assert response.status_code >= 400
