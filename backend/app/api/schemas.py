import datetime
from typing import List

from pydantic import BaseModel


class DisplayWeatherData(BaseModel):
    date: List[datetime.datetime]
    temp: List[float]
    pressure: List[float]
    humidity: List[float]
    feels_like: List[float]
    speed: List[float]
