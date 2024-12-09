import requests
import Flask
from rich import print

api_url = 'https://dataservice.accuweather.com/'
loc_url = '/locations/v1/cities/geoposition/search'
api_key = 'UGH2Z3Su53KsHjpz6PT6wcKd5ueF3b77'

latitude = input('Введите широту: ')
longitude = input('Введите долготу: ')

loc_key = requests.get(api_url + loc_url,
                       params = {
                           'q': f'{latitude},{longitude}',
                           'apikey': api_key
                       }).json()['Key']

w_url = f'/currentconditions/v1/{loc_key}'
r_w = requests.get(api_url + w_url, params={'details': 'true',
                                            'apikey': api_key}).json()

rain_url = f'/forecasts/v1/daily/1day/{loc_key}'
r_rain = requests.get(api_url + rain_url, params={'details': 'true',
                                               'apikey': api_key}).json()
print(r_rain)

temp = r_w[0]['Temperature']['Metric']['Value']
print('Температура:', temp, 'C')

humidity = r_w[0]['RelativeHumidity']
print('Влажность:', humidity, '%')

wind = r_w[0]['Wind']['Speed']['Metric']['Value']
print('Скорость ветра:', wind, 'km/h')

rain = r_rain['DailyForecasts'][0]['Day']['RainProbability']
print('Вероятность дождя:', rain)


