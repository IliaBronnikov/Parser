import pytest
from fastapi.testclient import TestClient
from parser import app

def test_start_page():
    client = TestClient(app)

    response = client.get("/")
    content = response.content.decode("utf-8")

    assert response.status_code == 200
    assert "Please use" in content

def test_text_page():
    client = TestClient(app)
    url = "https://habr.com/ru/company/epam_systems/news/t/589555/"

    response = client.get("/text?url={}".format(url))
    content = response.content.decode("utf-8")

    assert response.status_code == 200
    assert "Программа разработана для детей" in content
