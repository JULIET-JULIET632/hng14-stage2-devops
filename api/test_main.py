import pytest
from fastapi.testclient import TestClient
from unittest.mock import MagicMock, patch
import sys
import os

sys.path.insert(0, os.path.dirname(__file__))

# Mock redis before importing app
with patch('redis.Redis') as mock_redis:
    mock_redis.return_value = MagicMock()
    from main import app, r

client = TestClient(app)

@pytest.fixture(autouse=True)
def mock_redis_client():
    r.lpush = MagicMock()
    r.hset = MagicMock()
    r.hget = MagicMock()

def test_create_job():
    response = client.post("/jobs")
    assert response.status_code == 200
    data = response.json()
    assert "job_id" in data
    assert len(data["job_id"]) > 0

def test_get_job_found():
    r.hget.return_value = b"queued"
    response = client.get("/jobs/test-job-123")
    assert response.status_code == 200
    data = response.json()
    assert data["job_id"] == "test-job-123"
    assert data["status"] == "queued"

def test_get_job_not_found():
    r.hget.return_value = None
    response = client.get("/jobs/nonexistent-job")
    assert response.status_code == 200
    data = response.json()
    assert "error" in data
    assert data["error"] == "not found"

def test_create_job_pushes_to_queue():
    response = client.post("/jobs")
    assert response.status_code == 200
    assert r.lpush.called

def test_create_job_sets_status():
    response = client.post("/jobs")
    assert response.status_code == 200
    assert r.hset.called
