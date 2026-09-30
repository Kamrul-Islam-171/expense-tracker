# Expense Tracker API

A Personal Expense Tracker API built with FastAPI, SQLAlchemy, and PostgreSQL. Users can register, log in, and manage their own income/expense transactions, with JWT-protected routes and per-user data isolation.

## Features

- User registration and login with hashed passwords (`pwdlib`)
- JWT-based authentication (`python-jose`)
- Full CRUD for transactions, scoped to the authenticated user
- Filtering transactions by `type`, `category`, `minimum_amount`, and `maximum_amount`
- PostgreSQL persistence via SQLAlchemy ORM
- Pytest test suite using an in-memory SQLite database

## Tech Stack

- **Framework:** FastAPI
- **ORM:** SQLAlchemy
- **Database:** PostgreSQL
- **Auth:** OAuth2 Password Flow + JWT
- **Testing:** Pytest, FastAPI `TestClient`

## Project Structure

```
app/
  main.py            # FastAPI app entrypoint
  auth.py             # Password hashing, JWT creation/verification, current-user dependency
  database.py          # SQLAlchemy engine/session setup
  models.py            # User and Transaction ORM models
  schemas.py           # Pydantic request/response models
  routers/
    auth.py            # /auth/register, /auth/login
    transactions.py     # /transactions CRUD + /transactions/filter
tests/
  test_transactions.py  # Pytest test cases
```

## Setup

### 1. Clone and create a virtual environment

```bash
git clone <repo-url>
cd expense-tracker
python -m venv venv
venv\Scripts\activate       # Windows
source venv/bin/activate    # macOS/Linux
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Configure environment variables

Copy `.env.example` to `.env` and fill in your own values:

```
DATABASE_URL=postgresql://<user>:<password>@<host>:<port>/<database>
SECRET_KEY=<a-strong-random-secret>
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

### 4. Run the app

```bash
uvicorn app.main:app --reload
```

The API will be available at `http://127.0.0.1:8000`, with interactive docs at `http://127.0.0.1:8000/docs`.

## API Endpoints

### Authentication

| Method | Endpoint | Description |
|---|---|---|
| POST | `/auth/register` | Register a new user |
| POST | `/auth/login` | Log in and receive a JWT access token |

### Transactions (require `Authorization: Bearer <token>`)

| Method | Endpoint | Description |
|---|---|---|
| POST | `/transactions` | Create a transaction |
| GET | `/transactions` | List the current user's transactions |
| GET | `/transactions/filter` | Filter transactions by `type`, `category`, `minimum_amount`, `maximum_amount` |
| GET | `/transactions/{transaction_id}` | Get a single transaction |
| PUT | `/transactions/{transaction_id}` | Update a transaction |
| DELETE | `/transactions/{transaction_id}` | Delete a transaction |

## Running Tests

```bash
pytest
```

Tests run against an isolated in-memory SQLite database and cover: create, list, get-by-id, update, and delete transaction flows.

## Deployment (Render)

1. Push the repository to GitHub.
2. Create a new **Web Service** on [Render](https://render.com) and connect the repo.
3. Set the build command:
   ```
   pip install -r requirements.txt
   ```
4. Set the start command:
   ```
   uvicorn app.main:app --host 0.0.0.0 --port $PORT
   ```
5. Add the environment variables from `.env.example` (`DATABASE_URL`, `SECRET_KEY`, `ALGORITHM`, `ACCESS_TOKEN_EXPIRE_MINUTES`) in the Render dashboard, pointing `DATABASE_URL` at your hosted PostgreSQL instance.
6. Deploy. Render will build and start the service automatically on each push.
