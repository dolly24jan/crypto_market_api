from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)
VALID_AUTH = ("admin", "secret")
INVALID_AUTH = ("admin", "wrongpass")


# Root endpoint
def test_root():
    response = client.get("/")
    assert response.status_code == 200
    assert "Welcome to the Crypto Market API" in response.json()["message"]


# Health check
def test_health_check():
    response = client.get("/health")
    assert response.status_code == 200
    json = response.json()
    assert json["app_status"] == "healthy"
    assert "coingecko_status" in json


# Version check
def test_version_info():
    response = client.get("/version")
    assert response.status_code == 200
    assert response.json() == {"version": "1.0.0"}


# Unauthorized access
def test_unauthenticated_access_denied():
    response = client.get("/coins")
    assert response.status_code == 401
    assert response.json()["detail"] == "Not authenticated"


def test_invalid_credentials_access_denied():
    response = client.get("/coins", auth=INVALID_AUTH)
    assert response.status_code == 401
    assert response.json()["detail"] == "Incorrect username or password"



# /coins
def test_list_coins():
    response = client.get("/coins", auth=VALID_AUTH)
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert all("id" in coin for coin in data)


# /categories
def test_list_categories():
    response = client.get("/categories", auth=VALID_AUTH)
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert all("category_id" in cat or "name" in cat for cat in data)


# /coins/filter
def test_filter_coins_no_filter():
    response = client.get("/coins/filter", auth=VALID_AUTH)
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_filter_coins_by_ids():
    response = client.get("/coins/filter?ids=bitcoin", auth=VALID_AUTH)
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert any("bitcoin" in coin["id"] for coin in data)


