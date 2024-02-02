import unittest
from unittest.mock import patch, AsyncMock
from fastapi.testclient import TestClient
from backend.app.api.router import router
from backend.app.api.schemas import DisplayWeatherData
import datetime
import asynctest

client = TestClient(router)


class TestWeatherPrediction(asynctest.TestCase):
    @patch('backend.app.api.router.get_weather_prediction_data')
    async def test_get_weather_prediction_data_positive(self, mocked_get):
        current_datetime = datetime.datetime(2024, 2, 2, 21, 44, 8, 508475)
        date_list = [current_datetime]
        mock_data = DisplayWeatherData(
            date=date_list,
            temp=[20.0],
            pressure=[1013],
            humidity=[50],
            feels_like=[18.0],
            speed=[5.0]
        )
        mocked_get.return_value = mock_data

        response = client.get(
            "/api/v1/get_weather_prediction?lat=42.0&lon=24.0")

        self.assertEqual(response.status_code, 200)

        response_data = response.json()
        response_date = [datetime.datetime.fromisoformat(
            date) for date in response_data['date']]

        self.assertEqual(response_data['temp'], mock_data.temp)
        self.assertEqual(response_data['pressure'], mock_data.pressure)
        self.assertEqual(response_data['humidity'], mock_data.humidity)
        self.assertEqual(response_data['feels_like'], mock_data.feels_like)
        self.assertEqual(response_data['speed'], mock_data.speed)
        self.assertEqual(response_date, mock_data.date)

    @patch('backend.app.api.router.get_weather_prediction_data')
    async def test_get_weather_prediction_data_negative(self, mocked_get):
        mock_data = None
        mocked_get.return_value = mock_data

        response = client.get(
            "/api/v1/get_weather_prediction?lat=42.0&lon=24.0")

        self.assertNotEqual(response.status_code, 200)
        self.assertEqual(response.json(), {
                         "message": "Check your API key or params"})


if __name__ == '__main__':
    unittest.main()
