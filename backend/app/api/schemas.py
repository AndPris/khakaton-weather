import datetime
from typing import List

from pydantic import BaseModel


class DisplayWeatherData(BaseModel):
    date: List[datetime.datetime]
    temp: List[float]
    pressure: List[float]
    humidity: List[float]
    temp_min: List[float]
    temp_max: List[float]
    feels_like: List[float]
    speed: List[float]
    deg: List[float]
    gust: List[float]
    all: List[float]
