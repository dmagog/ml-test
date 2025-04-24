from fastapi.testclient import TestClient
import pytest
from sqlmodel import Session 
from models.user import User
from services.crud.user import *
from models.billing import Bill, BillOperation
import pytest
from routes.billing import *

def test_home_request(client: TestClient):
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "healthy"}
    
def test_get_privat(client: TestClient):
    response = client.get("/api/users/get_all_users")
    assert response.status_code == 200
    assert response.json() == []
    
    

def test_get_user_by_id_success(client: TestClient, session: Session):
    user = User(
        id=1,
        name="Alice",
        password="hashedpassword",
        email="alice@example.com",
        age=30
    )
    session.add(user)
    session.commit()

    response = client.get("/api/users/id/1")
    assert response.status_code == 200
    data = response.json()
    assert data["email"] == "alice@example.com"
    assert data["name"] == "Alice"

def test_get_user_by_id_not_found(client: TestClient):
    response = client.get("/api/users/id/999")
    assert response.status_code == 404
    assert response.json()["detail"] == "Users with supplied ID does not exist"

    
def test_get_bill_by_id_success(client: TestClient, session: Session):
    bill = Bill(
        id=1,
        balance=250.50,
        freeLimit_today=2,
        freeLimit_perDay=3,
    )
    session.add(bill)
    session.commit()

    response = client.get("/api/billing/1")  # убедись, что роут подключён как /billing
    assert response.status_code == 200
    data = response.json()

    assert data["id"] == 1
    assert data["balance"] == 250.50
    assert data["freeLimit_today"] == 2
    assert data["freeLimit_perDay"] == 3

def test_get_bill_by_id_not_found(client: TestClient, session: Session):
    response = client.get("/api/billing/999")
    assert response.status_code == 404
    assert response.json()["detail"] == "Bill with supplied ID does not exist"
