import json

from fastapi.testclient import TestClient

from module_26_fastapi.homework.main import app

client = TestClient(app)


def test_read_main():
    response = client.get("/")
    assert response.status_code == 200


def test_get_list_recepts():
    response = client.get("/recepts")
    assert response.status_code == 200
    assert isinstance(response.json()[0].get('title'), str)
    assert isinstance(response.json()[0].get('time_cook'), int)


def test_get_one_recept():
    response = client.get("/recept/1")
    assert response.status_code == 200
    assert isinstance(response.json()[0].get('title'), str)
    assert isinstance(response.json()[0].get('time_cook'), int)
    assert len(response.json()) >= 1


def test_post_one_recept():
    test_record = {
      "title": "Тест",
      "time_cook": 60,
      "ingridients": "Тест Тест",
      "description": "Тест Тест"
    }
    response = client.post("/add_recept", data=json.dumps(test_record),)
    assert response.status_code == 201
