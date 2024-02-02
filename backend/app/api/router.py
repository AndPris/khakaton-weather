from typing import Dict, Union

from .schemas import DisplayWeatherData
from .utils import get_weather_prediction_data
from fastapi import APIRouter, Query
from fastapi.responses import JSONResponse

router = APIRouter(prefix="/api/v1")


@router.get(
    "/get_weather_prediction", response_model=Union[DisplayWeatherData, Dict[str, str]]
)
async def get_user_by_id(
    lat: float = Query(..., description="Latitude"),
    lon: float = Query(..., description="Longitude"),
):
    print(lat, lon)
    data = await get_weather_prediction_data(lon, lat)
    if not data:
        return JSONResponse(status_code=400, content={"message": "Check your API key or params"})

    return data
