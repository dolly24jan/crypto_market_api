## Crypto Market API

A FastAPI-based API that provides access to cryptocurrency data from CoinGecko. It allows users to list coins, categories, and markets, with support for filtering by coin IDs, categories, and pagination. Authentication is required for access.

## Features
- List all coins
- List coin categories
- Filter coins by ID or category
- Pagination support
- Auth protected (HTTP Basic)
- Health & Version endpoints
- Swagger docs at `/docs`
- Docker support

## Technologies Used

    Python 3.x
    FastAPI
    Requests library for making HTTP requests
    pytest for testing

## Folder Strucure

.
├── app/                   # Application folder containing the FastAPI app
│   ├── main.py            # Main FastAPI app file
├── tests/                 # Test suite for the application
│   ├── test_main.py       # Test cases for the main FastAPI app
├── requirements.txt       # Production dependencies (list of packages needed)
├── README.md              # This file with setup instructions
└── Dockerfile             # Docker setup for containerizing the app (if Dockerized)


## Setup

```bash
git clone <repo>
cd crypto_api_project
pip install -r requirements.txt
uvicorn app.main:app --reload
```
The API should now be running at `http://127.0.0.1:8000`


Create a .env file with the following configuration:

```env
COINGECKO_API_BASE=https://api.coingecko.com/api/v3
DEFAULT_CURRENCY=cad
```

## Docker Usage
### Build and Run
```bash
docker build -t crypto-api .
docker run -d -p 8000:8000 crypto-api
```

### Or with Docker Compose
To start both the application and related services:

```bash
docker-compose up --build
```


## Running Tests
pytest
