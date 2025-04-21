# main.py
from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from typing import List, Optional
import requests
import uvicorn
import secrets
import os


app = FastAPI(title="Crypto Market API", version="1.0.0")

security = HTTPBasic()

VALID_USERNAME = "admin"
VALID_PASSWORD = "secret"

# Basic Authentication
def authenticate(credentials: HTTPBasicCredentials = Depends(security)):
    correct_username = secrets.compare_digest(credentials.username, VALID_USERNAME)
    correct_password = secrets.compare_digest(credentials.password, VALID_PASSWORD)
    if not (correct_username and correct_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Basic"},
        )
    return credentials.username


@app.get("/")
def root():
    return {"message": "Welcome to the Crypto Market API. Visit /docs for documentation."}


@app.get("/coins", dependencies=[Depends(authenticate)])
def list_all_coins(page_num: int = 1, per_page: int = 10):
    url = f"https://api.coingecko.com/api/v3/coins/markets"
    params = {
        "vs_currency": "cad",
        "order": "market_cap_desc",
        "per_page": per_page,
        "page": page_num,
        "sparkline": False
    }
    response = requests.get(url, params=params)
    if response.status_code != 200:
        raise HTTPException(status_code=500, detail="CoinGecko API error")
    return response.json()


@app.get("/categories", dependencies=[Depends(authenticate)])
def list_categories():
    url = "https://api.coingecko.com/api/v3/coins/categories/list"
    response = requests.get(url)
    if response.status_code != 200:
        raise HTTPException(status_code=500, detail="CoinGecko API error")
    return response.json()


@app.get("/coins/filter", dependencies=[Depends(authenticate)])
def filter_coins(
    ids: Optional[str] = None,
    category: Optional[str] = None,
    page_num: int = 1,
    per_page: int = 10
):
    url = f"https://api.coingecko.com/api/v3/coins/markets"
    params = {
        "vs_currency": "cad",
        "order": "market_cap_desc",
        "per_page": per_page,
        "page": page_num,
        "sparkline": False
    }
    if ids:
        params["ids"] = ids
    if category:
        params["category"] = category

    response = requests.get(url, params=params)
    if response.status_code == 429:
        print("CoinGecko Rate Limit Hit:", response.text)
        raise HTTPException(status_code=429, detail="CoinGecko API rate limit exceeded")
    elif response.status_code != 200:
        print("CoinGecko Error:", response.status_code, response.text)
        raise HTTPException(status_code=500, detail="CoinGecko API error")
    return response.json()


@app.get("/health")
def health_check():
    try:
        response = requests.get("https://api.coingecko.com/api/v3/ping")
        coingecko_status = response.status_code == 200
    except Exception:
        coingecko_status = False
    return {"app_status": "healthy", "coingecko_status": coingecko_status}


@app.get("/version")
def version():
    return {"version": "1.0.0"}


# Run with: uvicorn main:app --reload
if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
