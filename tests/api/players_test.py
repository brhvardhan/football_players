import sys
import asyncio
from fastapi.testclient import TestClient
from main import app

if sys.platform == "win32" and (3, 8, 0) <= sys.version_info < (3, 9, 0):
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

client = TestClient(app)


def test_dummy_url():
    response = client.get("/")
    assert response.status_code == 404


def test_get_member():
    response = client.get("/player/1")
    assert response.status_code == 200
    expected_response = {
        "age": 25,
        "team_id": 1,
        "name": "Patrick Mahomes",
        "id": 1,
        "team": {
                "id": 1,
                "name": "Dark Pharaoahs"
        }
    }
    assert response.json() == expected_response


def test_get_member_with_invalid_id():
    response = client.get("/player/100000")
    assert response.status_code == 404
    expected_response = {
        "detail": "Member not found"
    }
    assert response.json() == expected_response


def test_get_member_with_invalid_format():
    response = client.get("/player/string")
    assert response.status_code == 422
    expected_response = {"detail": [{"loc": ["path", "id"],
                                     "msg":"value is not a valid integer",
                                     "type":"type_error.integer"}]}
    assert response.json() == expected_response


class TestMember:
    def test_workflow(self):
        member_id = self.create_member()
        self.update_member(member_id)
        self.delete_member(member_id)

    def create_member(self):
        dummy_body = {
            "name": "pytest-1",
            "age": 12,
            "team_name": "Onerous Tornados"
        }
        response = client.post("/create_player", json=dummy_body)
        assert response.status_code == 200
        response_body = response.json()
        self.member_id = response_body['id']
        assert response_body['name'] == dummy_body['name']
        assert response_body['age'] == dummy_body['age']
        assert response_body['team_id'] > 0
        assert response_body['id'] > 0
        return self.member_id

    def update_member(self, member_id):
        dummy_body = {
            "name": "pytest-1-updated",
            "age": 14,
            "team_id": 1
        }
        response = client.put(
            "/player/{id}".format(id=member_id), json=dummy_body)
        assert response.status_code == 200
        response_body = response.json()
        assert response_body == {"detail": "Record Updated Successfully."}
        response = client.get("/player/{id}".format(id=member_id))
        response_body = response.json()
        assert response_body['name'] == dummy_body['name']
        assert response_body['age'] == dummy_body['age']
        assert response_body['team_id'] > 0
        assert response_body['id'] > 0

    def delete_member(self, member_id):
        response = client.delete("/player/{id}".format(id=member_id))
        assert response.status_code == 204
        response = client.get("/player/{id}".format(id=member_id))
        assert response.status_code == 404


def test_create_member_with_invalid_team():
    dummy_body = {
        "name": "pytest-1",
        "age": 12,
        "team_name": "pytest"
    }
    response = client.post("/create_player", json=dummy_body)
    assert response.status_code == 400
    expected_response = {"detail": "Invalid Team Name"}
    assert response.json() == expected_response


def test_create_member_with_invalid_age():
    dummy_body = {
        "name": "pytest-1",
        "age": -12,
        "team_name": "pytest"
    }
    response = client.post("/create_player", json=dummy_body)
    assert response.status_code == 422
    expected_response = {
        "detail": [{"loc": ["body", "age"], "msg": "Age should not be negative", "type": "value_error"}]}
    assert response.json() == expected_response
