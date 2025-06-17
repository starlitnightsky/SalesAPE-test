from fastapi.testclient import TestClient
from app.main import app, extract_category

client = TestClient(app)

def test_read_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Welcome to Joke Search API"}

def test_get_joke():
    response = client.get("/api/joke/1")
    assert response.status_code == 200
    data = response.json()
    assert "type" in data
    assert "category" in data
    assert "safe" in data

def test_search_joke():
    response = client.get("/api/search?query=programming")
    assert response.status_code == 200
    data = response.json()
    assert "error" in data
    assert "category" in data

def test_get_categories():
    response = client.get("/api/categories")
    assert response.status_code == 200
    data = response.json()
    assert "categories" in data

def test_ask_for_joke():
    # Test programming joke request
    response = client.post("/api/ask", json={"request": "Tell me a programming joke"})
    assert response.status_code == 200
    data = response.json()
    assert "category" in data
    assert data["category"] == "Programming"
    assert "is_safe" in data

    # Test general joke request
    response = client.post("/api/ask", json={"request": "Tell me a joke"})
    assert response.status_code == 200
    data = response.json()
    assert "category" in data
    assert "is_safe" in data

def test_category_extraction():
    assert extract_category("Tell me a programming joke") == "Programming"
    assert extract_category("I want a dark joke") == "Dark"
    assert extract_category("Share a pun with me") == "Pun"
    assert extract_category("Any joke will do") == "Any" 