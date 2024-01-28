from functions import *

jsonData = pd.read_json('weather.json')
dataList = jsonData['list']

forecasts = []
for key in ['main', 'wind', 'clouds']:
    for property in dataList[0][key].keys():
        formattedData = getFormattedData(dataList, key, property)
        forecast = makeHourlyForecast(formattedData, property)
        forecasts.append(forecast)

globalForecast = forecasts[0]
for forecast in forecasts[1:]:
    globalForecast = pd.merge(globalForecast, forecast, on=dateAlias)
print(globalForecast)