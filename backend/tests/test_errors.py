from fastapi import APIRouter
from fastapi.testclient import TestClient
from app.core.errors import NotFoundError


def test_404_route_returns_standard_error_response(client):
    response = client.get("/api/v1/non-existent-endpoint")
    assert response.status_code == 404
    data = response.json()
    assert data["code"] == "HTTP_ERROR"
    assert "Not Found" in data["message"]
    assert "request_id" in data
    assert "timestamp" in data
    assert "X-Request-ID" in response.headers


def test_custom_app_exception_handling(client):
    test_router = APIRouter()

    @test_router.get("/trigger-app-exception")
    def trigger_error():
        raise NotFoundError(message="Bài học không tồn tại", details={"lesson_id": "les_999"})

    from app.main import app
    app.include_router(test_router, prefix="/api/v1/test-err")

    response = client.get("/api/v1/test-err/trigger-app-exception")
    assert response.status_code == 404
    data = response.json()
    assert data["code"] == "NOT_FOUND"
    assert data["message"] == "Bài học không tồn tại"
    assert data["details"]["lesson_id"] == "les_999"
    assert "timestamp" in data


def test_unhandled_exception_returns_500_with_standard_error():
    from app.main import app
    test_router = APIRouter()

    @test_router.get("/trigger-500")
    def trigger_crash():
        raise RuntimeError("Cố ý gây lỗi server nội bộ để kiểm thử handler")

    app.include_router(test_router, prefix="/api/v1/test-crash")

    client_no_raise = TestClient(app, raise_server_exceptions=False)
    response = client_no_raise.get("/api/v1/test-crash/trigger-500")
    assert response.status_code == 500
    data = response.json()
    assert data["code"] == "INTERNAL_SERVER_ERROR"
    assert "Hệ thống gặp sự cố" in data["message"]
    assert "request_id" in data
    assert "timestamp" in data
