from unittest.mock import patch, MagicMock
from app import app


def test_health():
    client = app.test_client()
    response = client.get("/health")
    assert response.status_code == 200


def test_health_says_ok():
    client = app.test_client()
    response = client.get("/health")
    assert b"OK" in response.data


@patch("app.db.get_connection")
def test_unknown_code_return_404(mock_get_connection):
    fake_cursor = MagicMock()
    fake_cursor.fetchone.return_value = None

    fake_conn = MagicMock()
    fake_conn.cursor.return_value = fake_cursor

    mock_get_connection.return_value = fake_conn
    client = app.test_client()
    response = client.get("/unknown_code")

    assert response.status_code == 404
