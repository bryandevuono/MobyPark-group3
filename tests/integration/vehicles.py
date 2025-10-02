import requests
import pytest

BASE_URL = "http://localhost:8000"

@pytest.fixture(scope="session")
def headers():
    payload = {
        "username": "johndoe",
        "password": "strongpassword123"
    }
    response = requests.post(f"{BASE_URL}/login", json=payload)
    response.raise_for_status()
    token = response.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}

# happy flow
def test___get_all_vehicles():
    payload = {
        "username": "johndoe",
        "password": "strongpassword123"
    }
    
    response = requests.post(f"{BASE_URL}/login", json=payload)
    json_response = response.json()
    key = json_response["access_token"]
    
    headers = {
        "Authorization": f'Bearer {key}'
    }

    response = requests.get(f"{BASE_URL}/vehicles", headers=headers)
    print(headers)
    assert response.status_code == 200

def test_add_vehicle(headers):
    payload = {
        "license_plate": "ADDD1235",
        "make": "toyota",
        "model": "corolla",
        "color": "Blue",
        "year": 2020
    }

    response = requests.post(f"{BASE_URL}/vehicles", headers=headers, json=payload)

    assert response.status_code in [200, 201], f"Unexpected response: {response.status_code}, {response.text} {headers}"

def test_get_vehicle(headers):
    response = requests.get(f"{BASE_URL}/vehicles/1", headers=headers)

    assert response.status_code == 200, headers

def test__update_vehicle(headers):
    payload = {
        "license_plate": "ABD123",
        "make": "toyota",
        "model": "corolla",
        "color": "Blue",
        "year": 2021
    }

    response = requests.put(f"{BASE_URL}/vehicles/1", headers=headers, json=payload)

    assert response.status_code == 200

def test_deleting_vehicle(headers): 
    response = requests.delete(f"{BASE_URL}/vehicles/1", headers=headers)

    assert response.status_code == 200

# sad flow
def test_get_vehicles_no_auth(): 
    payload = {
        "username": "", 
        "password": ""
    }
    
    response = requests.post(f"{BASE_URL}/login", json=payload)
    json_response = response.json()

    if "access_token" in json_response:
        access_token = json_response["access_token"]
    else:
        access_token = ""
    
    headers = {
        "Authorization": f"Bearer {access_token}"
    }
    response = requests.get(f"{BASE_URL}/vehicles", headers=headers)
    
    assert response.status_code != 200

def delete_non_existing_vehicle(headers):
    response = requests.delete(f"{BASE_URL}/vehicles/1000", headers=headers)

    assert response.status_code == 404

def test_get_non_existing_vehicle(headers):
    response = requests.get(f"{BASE_URL}/vehicles/1111", headers=headers)

    assert response.status_code == 200

def test_update_non_existing_vehicle(headers):
    payload = {
        "license_plate": "ABD123",
        "make": "toyota",
        "model": "corolla",
        "color": "Blue",
        "year": 2021
    }

    response = requests.put(f"{BASE_URL}/vehicles/111", headers=headers, json=payload)

    assert response.status_code == 404

def test_update_empty_string(headers):
    payload = {
        "license_plate": "",
        "make": "",
        "model": "corolla",
        "color": "Blue",
        "year": 2021
    }

    response = requests.put(f"{BASE_URL}/vehicles/111", headers=headers, json=payload)

    assert response.status_code >= 400