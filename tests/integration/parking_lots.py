import requests

BASE_URL = "http://localhost:8000"

# happy flow
def test_get_parking_lots():
    payload = {
        "username": "meneer4", 
        "password": "secret"
    }
    
    requests.post(f"{BASE_URL}/register", json=payload)
    response = requests.post(f"{BASE_URL}/login", json=payload)
    json_response = response.json()
    session_token = json_response["session_token"]
    print(session_token)
    
    headers = {
        "Authorization": session_token
    }
    response = requests.get(f"{BASE_URL}/parking-lots", headers=headers)
    
    assert response.status_code == 200

def test_get_parking_lots():
    payload = {
        "username": "meneer5", 
        "password": "secret"
    }
    
    requests.post(f"{BASE_URL}/register", json=payload)
    response = requests.post(f"{BASE_URL}/login", json=payload)
    json_response = response.json()
    session_token = json_response["session_token"]
    print(session_token)
    
    headers = {
        "Authorization": session_token
    }
    response = requests.get(f"{BASE_URL}/parking-lots/1", headers=headers)
    
    assert response.status_code == 200

# sad flow

def test_get_parking_lots_no_token():
    payload = {
        "username": "meneer5", 
        "password": "secret"
    }
    
    requests.post(f"{BASE_URL}/register", json=payload)
    response = requests.post(f"{BASE_URL}/login", json=payload)
    json_response = response.json()
    session_token = json_response["session_token"]
    print(session_token)
    
    headers = {
        "Authorization": ""
    }
    response = requests.get(f"{BASE_URL}/parking-lots/1", headers=headers)
    
    assert response.status_code == 200