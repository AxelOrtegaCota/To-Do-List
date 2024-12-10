import pytest
from app.utils.jokes import fetch_joke

def test_fetch_joke(monkeypatch):
    """Test fetching a joke with a mocked API response."""
    class MockResponse:
        @staticmethod
        def json():
            return {
                "error": False,
                "type": "single",
                "joke": "Why don't programmers like nature? It has too many bugs."
            }

        @staticmethod
        def raise_for_status():
            pass  # Simula que la respuesta es exitosa y no lanza excepciones

    def mock_get(*args, **kwargs):
        return MockResponse()

    monkeypatch.setattr("requests.get", mock_get)

    joke = fetch_joke(category="Programming", joke_type="single")
    assert not joke.get("error")
    assert joke["type"] == "single"
    assert "joke" in joke

