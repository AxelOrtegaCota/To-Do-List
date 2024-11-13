# tests/unit/test_services/test_weather_service.py
import pytest
from app.services.weather_service import get_weather_data

def test_get_weather_data():
    weather = get_weather_data('New York')
    assert 'temperature' in weather
    assert weather['temperature'] > -50  # Valor esperado de temperatura
