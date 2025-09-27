import requests

BASE_URL = "http://localhost:8000"

# happy flow
def test_see_profile():
    payload = {
        "username": "meneer3", 
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
    response = requests.get(f"{BASE_URL}/profile", headers=headers)
    
    assert response.status_code == 200

# sad flow

def test_see_profile_no_token():
    payload = {
        "username": "meneer3", 
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
    response = requests.get(f"{BASE_URL}/profile", headers=headers)
    
    assert response.status_code == 401