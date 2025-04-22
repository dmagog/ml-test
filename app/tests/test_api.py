from fastapi.testclient import TestClient
import pytest

def test_home_request(client: TestClient):
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "healthy"}
    
def test_get_privat(client: TestClient):
    response = client.get("/api/users/get_all_users")
    assert response.status_code == 200
    assert response.json() == []
    
def test_create_user_bad(client: TestClient):
    user_data = {
        "name": "name",
        "email": "test121@mail.ru",
    }
    
    with pytest.raises(Exception) as ex:
        response = client.post("/api/users/signin", json=user_data)

        assert response.status_code == 200
        assert response.json() == {"message": "User created unsuccessfully"}
    
    
def test_get_user_by_id(client: TestClient):
    with pytest.raises(Exception) as ex:
        response = client.get("/api/users/id/9999")
        assert response.status_code == 200


def test_get_user_by_email(client: TestClient):
    with pytest.raises(Exception) as ex:
        response = client.get("/api/users/email/test199@mail.ru")
        assert response.status_code == 200
