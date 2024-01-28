import pandas as pd
from datetime import datetime, timezone, timedelta
from prophet import Prophet

dateAlias = 'date time'

def getFormattedData(dataList, weatherComponent, criteria):
    formattedData = []

    for entry in dataList:
        timestamp = entry['dt']
        temperature = entry[weatherComponent][criteria]

        date = datetime.fromtimestamp(timestamp, tz=timezone.utc).strftime('%Y-%m-%d %H:%M:%S')

        formattedData.append({'ds': date, 'y': temperature})

    return formattedData


def makeHourlyForecast(formattedData, alias):
    weatherData = getWeatherData(formattedData)

    model = Prophet()
    model.fit(weatherData)

    lastDate = weatherData['ds'].iloc[-1]
    lastDate = pd.to_datetime(lastDate)

    nextDay = lastDate + timedelta(days=1)
    nextDayHours = pd.date_range(start=nextDay.replace(hour=0, minute=0, second=0, microsecond=0),
                                end=nextDay.replace(hour=23, minute=59, second=59, microsecond=999),
                                freq='h').tz_localize(None)

    futureHourly = pd.DataFrame({'ds': nextDayHours})
    forecastHourly = model.predict(futureHourly)

    forecastHourly = forecastHourly.rename(columns={'ds': dateAlias})
    forecastHourly = forecastHourly.rename(columns={'yhat': alias})

    return forecastHourly[[dateAlias, alias]]


def getWeatherData(formattedData):
    weatherData = pd.DataFrame(formattedData)
    weatherData = weatherData.sort_values(by='ds')
    return weatherData