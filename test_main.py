from fastapi.testclient import TestClient
import pytest
from main import app, STOCK_PRICES

# Create a simulated client to hit our API without running a live server
client = TestClient(app)

def test_successful_order():
    """Verify that a user with enough balance can purchase a stock."""
    # Send a simulated GET request to buy 10 shares of Apple
    response = client.get("/buy?ticker=AAPL&quantity=10")
    
    # Assertions: Confirm we get a 200 OK status code
    assert response.status_code == 200
    
    data = response.json()
    assert data["status"] == "Order Placed Successfully"
    assert data["ticker"] == "AAPL"
    assert data["quantity"] == 10
    assert data["remaining_balance"] == 3250.00  # $5000 - ($175 * 10)

def test_insufficient_funds():
    """Verify that the system blocks an order if funds are too low."""
    # Send a request to buy 100 shares of Apple ($17,500 total cost)
    response = client.get("/buy?ticker=AAPL&quantity=100")
    
    # Assertions: Confirm the system returns a 400 Bad Request
    assert response.status_code == 400
    
    data = response.json()
    assert "Insufficient funds" in data["detail"]
