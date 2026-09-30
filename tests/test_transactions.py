import pytest

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from fastapi.testclient import TestClient

from app.main import app
from app.database import Base, get_db


# Test database
SQLALCHEMY_DATABASE_URL = "sqlite://"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool
)

TestingSessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)


def override_get_db():
    db = TestingSessionLocal()

    try:
        yield db
    finally:
        db.close()


# Use test database instead of PostgreSQL
app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)


@pytest.fixture(autouse=True)
def reset_database():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)

    yield


def get_auth_headers():
    # Register user
    client.post(
        "/auth/register",
        json={
            "username": "testuser",
            "email": "test@example.com",
            "password": "password123"
        }
    )

    # Login
    response = client.post(
        "/auth/login",
        data={
            "username": "testuser",
            "password": "password123"
        }
    )

    token = response.json()["access_token"]

    return {
        "Authorization": f"Bearer {token}"
    }


def create_test_transaction(headers):
    return client.post(
        "/transactions",
        json={
            "title": "Lunch",
            "amount": 500,
            "type": "expense",
            "category": "Food",
            "date": "2026-09-30"
        },
        headers=headers
    )


# --------------------------------
# 1. Create transaction
# --------------------------------

def test_create_transaction():
    headers = get_auth_headers()

    response = create_test_transaction(headers)

    assert response.status_code == 201

    data = response.json()

    assert data["title"] == "Lunch"
    assert data["amount"] == 500
    assert data["type"] == "expense"
    assert data["category"] == "Food"


# --------------------------------
# 2. Get all transactions
# --------------------------------

def test_get_transactions():
    headers = get_auth_headers()

    create_test_transaction(headers)

    response = client.get(
        "/transactions",
        headers=headers
    )

    assert response.status_code == 200

    data = response.json()

    assert len(data) == 1
    assert data[0]["title"] == "Lunch"


# --------------------------------
# 3. Get specific transaction
# --------------------------------

def test_get_specific_transaction():
    headers = get_auth_headers()

    create_response = create_test_transaction(headers)

    transaction_id = create_response.json()["id"]

    response = client.get(
        f"/transactions/{transaction_id}",
        headers=headers
    )

    assert response.status_code == 200

    data = response.json()

    assert data["id"] == transaction_id
    assert data["title"] == "Lunch"


# --------------------------------
# 4. Update transaction
# --------------------------------

def test_update_transaction():
    headers = get_auth_headers()

    create_response = create_test_transaction(headers)

    transaction_id = create_response.json()["id"]

    response = client.put(
        f"/transactions/{transaction_id}",
        json={
            "title": "Dinner",
            "amount": 800,
            "type": "expense",
            "category": "Food",
            "date": "2026-09-30"
        },
        headers=headers
    )

    assert response.status_code == 200

    data = response.json()

    assert data["title"] == "Dinner"
    assert data["amount"] == 800


# --------------------------------
# 5. Delete transaction
# --------------------------------

def test_delete_transaction():
    headers = get_auth_headers()

    create_response = create_test_transaction(headers)

    transaction_id = create_response.json()["id"]

    response = client.delete(
        f"/transactions/{transaction_id}",
        headers=headers
    )

    assert response.status_code == 200

    # Verify transaction was deleted
    get_response = client.get(
        f"/transactions/{transaction_id}",
        headers=headers
    )

    assert get_response.status_code == 404