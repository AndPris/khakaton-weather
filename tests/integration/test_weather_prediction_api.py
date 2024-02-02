import requests
from typing import Dict
from backend.app.api.schemas import DisplayWeatherData
from datetime import datetime
from pydantic import ValidationError, TypeAdapter


def get_endpoint(lon, lat):
    return f"http://127.0.0.1:8000/api/v1/get_weather_prediction?lon={lon}&lat={lat}"


def test_can_call_get_weather_with_correct_arguments():
    coords = [24.1051846, 56.9493977]
    response = requests.get(get_endpoint(coords[0], coords[1]))
    assert response.status_code == 200
    pass


def test_can_call_get_weather_with_incorrect_arguments():
    coords = ['ABC', 6000]
    response = requests.get(get_endpoint(coords[0], coords[1]))
    assert response.status_code == 400 or response.status_code == 422
    pass


def test_response_type_of_get_weather_prediction():
    coords = [24.1051846, 56.9493977]
    response = requests.get(get_endpoint(coords[0], coords[1]))
    response_data = response.json()

    try:
        weather_data = TypeAdapter(
            DisplayWeatherData).validate_python(response_data)
        print("Response matches DisplayWeatherData")
    except ValidationError as e:
        try:
            error_message = TypeAdapter(
                Dict[str, str]).validate_python(response_data)
            print("Response is a dictionary with string keys and values")
        except ValidationError:
            assert False, f"Response data does not match the expected types: {e}"
    pass


def test_response_content_of_get_weather_prediction():
    coords = [24.1051846, 56.9493977]
    response = requests.get(get_endpoint(coords[0], coords[1]))
    response_data = response.json()

    try:
        weather_data = TypeAdapter(
            DisplayWeatherData).validate_python(response_data)
        print("Response matches DisplayWeatherData")

        assert weather_data.date and all(isinstance(
            d, datetime) for d in weather_data.date), "Date list is empty or has invalid elements"
        assert weather_data.temp and all(isinstance(
            t, float) for t in weather_data.temp), "Temperature list is empty or has invalid elements"
        assert weather_data.pressure and all(isinstance(
            p, float) for p in weather_data.pressure), "Pressure list is empty or has invalid elements"
        assert weather_data.humidity and all(isinstance(
            h, float) for h in weather_data.humidity), "Humidity list is empty or has invalid elements"
        assert weather_data.feels_like and all(isinstance(
            f, float) for f in weather_data.feels_like), "Feels_like list is empty or has invalid elements"
        assert weather_data.speed and all(isinstance(
            s, float) for s in weather_data.speed), "Speed list is empty or has invalid elements"

    except ValidationError as e:
        try:
            error_message = TypeAdapter(
                Dict[str, str]).validate_python(response_data)
            print("Response is a dictionary with string keys and values")
        except ValidationError:
            assert False, f"Response data does not match the expected types: {e}"
