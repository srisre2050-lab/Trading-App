from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse

app = FastAPI(title="Trading Order Management System")

# Mock Database: Available cash balance and real-time security prices
ACCOUNT_BALANCE = 5000.00  
STOCK_PRICES = {
    "AAPL": 175.00,
    "TSLA": 180.00,
    "MSFT": 420.00,
    "NVDA": 900.00
}

@app.get("/")
def home():
    return {"message": "Welcome to the Trading OMS. Use /buy to place an order."}

@app.get("/buy")
def buy_security(ticker: str, quantity: int):
    global ACCOUNT_BALANCE
    
    ticker = ticker.upper()
    
    # 1. Validation: Does the stock exist?
    if ticker not in STOCK_PRICES:
        raise HTTPException(status_code=404, detail=f"Ticker {ticker} not found.")
        
    # 2. Validation: Is the quantity valid?
    if quantity <= 0:
        raise HTTPException(status_code=400, detail="Quantity must be greater than 0.")

    # 3. Risk Assessment: Calculate total cost
    price_per_share = STOCK_PRICES[ticker]
    total_cost = price_per_share * quantity

    # 4. Core Validation: Check account balance
    if ACCOUNT_BALANCE < total_cost:
        raise HTTPException(
            status_code=400, 
            detail=f"Insufficient funds. Cost: ${total_cost:,.2f}, Available: ${ACCOUNT_BALANCE:,.2f}"
        )

    # 5. Execution: Deduct funds
    ACCOUNT_BALANCE -= total_cost

    # 6. Response: Order placed successfully (200 OK)
    return JSONResponse(
        status_code=200,
        content={
            "status": "Order Placed Successfully",
            "ticker": ticker,
            "quantity": quantity,
            "price_per_share": price_per_share,
            "total_cost": total_cost,
            "remaining_balance": ACCOUNT_BALANCE
        }
    )
    # Trigger CI pipeline force scan

