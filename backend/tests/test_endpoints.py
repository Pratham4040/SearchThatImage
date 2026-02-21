"""Endpoint tests for image upload, search, and retrieval."""

from __future__ import annotations

import io

import pytest

from app.services import image_service


def _mock_tags(_: str) -> list[str]:
    return ["cat", "pet", "furry", "animal", "cute"]


def test_list_images_empty(client):
    response = client.get("/api/images/")
    assert response.status_code == 200
    payload = response.get_json()
    assert payload["images"] == []
    assert payload["total"] == 0


def test_upload_missing_file_field(client):
    response = client.post("/api/images/upload", data={})
    assert response.status_code == 400
    payload = response.get_json()
    assert payload["error"] == "No image field in request"


def test_upload_empty_filename(client):
    data = {"image": (io.BytesIO(b"data"), "")}
    response = client.post("/api/images/upload", data=data)
    assert response.status_code == 400
    payload = response.get_json()
    assert payload["error"] == "No file selected"


def test_upload_invalid_extension(client):
    data = {"image": (io.BytesIO(b"data"), "file.txt")}
    response = client.post("/api/images/upload", data=data)
    assert response.status_code == 400
    payload = response.get_json()
    assert "File type not allowed" in payload["error"]


def test_upload_and_serve_image(client, monkeypatch: pytest.MonkeyPatch):
    monkeypatch.setattr(image_service, "generate_image_tags", _mock_tags)

    data = {"image": (io.BytesIO(b"fake-image"), "photo.jpg")}
    response = client.post("/api/images/upload", data=data)
    assert response.status_code == 201
    payload = response.get_json()
    assert payload["filename"].endswith(".jpg")
    assert payload["tags"] == _mock_tags("unused")

    image_id = payload["id"]
    filename = payload["filename"]

    get_response = client.get(f"/api/images/{image_id}")
    assert get_response.status_code == 200

    file_response = client.get(f"/api/images/file/{filename}")
    assert file_response.status_code == 200


def test_search_missing_query(client):
    response = client.get("/api/search/")
    assert response.status_code == 400
    payload = response.get_json()
    assert payload["error"] == "Query parameter 'q' is required"


def test_search_returns_results(client, monkeypatch: pytest.MonkeyPatch):
    monkeypatch.setattr(image_service, "generate_image_tags", _mock_tags)
    data = {"image": (io.BytesIO(b"fake-image"), "photo.jpg")}
    client.post("/api/images/upload", data=data)

    response = client.get("/api/search/?q=cat")
    assert response.status_code == 200
    payload = response.get_json()
    assert payload["count"] == 1
    assert payload["results"][0]["tags"]


def test_limit_capped_at_100(client):
    response = client.get("/api/images/?page=1&limit=1000")
    assert response.status_code == 200
    payload = response.get_json()
    assert payload["limit"] == 100
