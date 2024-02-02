import datetime

import aiohttp
import pandas as pd
from ..config import API_WEATHER
from prophet import Prophet


async def get_weather_prediction_data(lon: float, lat: float):
    async with aiohttp.ClientSession() as session:
        start_date = datetime.datetime.timestamp(
            datetime.datetime.now() - datetime.timedelta(7)
        )
        end_date = datetime.datetime.timestamp(datetime.datetime.now())

        url = "https://history.openweathermap.org/data/2.5/history/city"
        params = {
            "lat": lat,
            "lon": lon,
            "start": int(start_date),
            "end": int(end_date),
            "units": "metric",
            "appid": API_WEATHER,
        }

        async with session.get(url, params=params) as resp:
            weather_data = await resp.json()
            if not weather_data:
                return None
            return await get_prediction_data(weather_data)


async def get_formatted_data(data_list, weather_component, criteria):
    formatted_data = []
    for entry in data_list:
        timestamp = entry["dt"]
        temperature = entry[weather_component][criteria]

        date = datetime.datetime.fromtimestamp(
            timestamp, tz=datetime.timezone.utc
        ).strftime("%Y-%m-%d %H:%M:%S")
        formatted_data.append({"ds": date, "y": temperature})

    return formatted_data


async def make_hourly_forecast(formatted_data, alias):
    weather_data = await get_weather_data(formatted_data)

    model = Prophet()
    model.fit(weather_data)

    last_date = weather_data["ds"].iloc[-1]
    last_date = pd.to_datetime(last_date)

    next_day = last_date + datetime.timedelta(days=1)
    next_day_hours = pd.date_range(
        start=next_day.replace(hour=0, minute=0, second=0, microsecond=0),
        end=next_day.replace(hour=23, minute=59, second=59, microsecond=999),
        freq="h",
    ).tz_localize(None)

    future_hourly = pd.DataFrame({"ds": next_day_hours})
    forecast_hourly = model.predict(future_hourly)

    forecast_hourly = forecast_hourly.rename(columns={"ds": "date_time"})
    forecast_hourly = forecast_hourly.rename(columns={"yhat": alias})

    return forecast_hourly[["date_time", alias]]


async def get_weather_data(formatted_data):
    weather_data = pd.DataFrame(formatted_data)
    weather_data = weather_data.sort_values(by="ds")
    return weather_data


async def get_prediction_data(json_data):
    try:
        data_list = json_data["list"]
        forecasts = []
        for key in ["main", "wind", "clouds"]:
            for option in data_list[0][key].keys():
                try:
                    print(f"Processing key: {key}, option: {option}")
                    formatted_data = await get_formatted_data(data_list, key, option)
                    forecast = await make_hourly_forecast(formatted_data, option)
                    forecasts.append(forecast)
                    print(f"Processed key: {key}, option: {option}")
                except KeyError as e:
                    print(
                        f"KeyError: {e} occurred for key: {key}, option: {option}")
                    # Handle the KeyError or add more specific error handling
                except Exception as e:
                    print(f"Exception Type: {type(e).__name__}")

        global_forecast = forecasts[0]
        for forecast in forecasts[1:]:
            global_forecast = pd.merge(
                global_forecast, forecast, on="date_time")

        dates = [date.to_pydatetime() for date in global_forecast["date_time"]]

        return {
            "date": dates[2::3],
            "temp": global_forecast["temp"].tolist()[2::3],
            "feels_like": global_forecast["feels_like"].tolist()[2::3],
            "pressure": global_forecast["pressure"].tolist()[2::3],
            "humidity": global_forecast["humidity"].tolist()[2::3],
            "speed": global_forecast["speed"].tolist()[2::3],
        }
    except Exception as e:
        print(f"Exception Type: {type(e).__name__}")
        return None
