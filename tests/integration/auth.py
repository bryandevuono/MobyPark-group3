import requests

BASE_URL = "http://localhost:8000"  

# happy flow 
def test_create_user():
    payload = {"username": "meneer", "password": "secret"}
    response = requests.post(f"{BASE_URL}/register", json=payload)

    assert response.status_code == 200

def test_login():
    payload = {"username": "meneer", "password": "secret"}
    response = requests.post(f"{BASE_URL}/login", json=payload)
    
    assert response.status_code == 200
    
# sad flow
