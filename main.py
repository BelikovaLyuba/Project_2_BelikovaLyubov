import requests
from flask import Flask, render_template, request

app = Flask(__name__)

api_url = 'https://dataservice.accuweather.com/'
api_key = 'bCd4AScdlmAAkBxbVo9NJqhhGC3wFdF5'
loc_url = 'locations/v1/cities/geoposition/search'
city_url = 'locations/v1/cities/search'

def find_loc_key(url, data):
    loc_key = requests.get(api_url + url,
                           params={
                               'q': data,
                               'apikey': api_key
                           }).json()
    return loc_key

def check_bad_weather(temp, wind, rain):
    if 0 <= temp <= 35 and wind <= 50 and rain <= 70:
        return False
    return True

def check(loc_key):
    w_url = f'/currentconditions/v1/{loc_key}'
    r_w = requests.get(api_url + w_url, params={'details': 'true',
                                                'apikey': api_key}).json()

    rain_url = f'/forecasts/v1/daily/1day/{loc_key}'
    r_rain = requests.get(api_url + rain_url, params={'details': 'true',
                                                      'apikey': api_key}).json()

    temp = r_w[0]['Temperature']['Metric']['Value']

    humidity = r_w[0]['RelativeHumidity']

    wind = r_w[0]['Wind']['Speed']['Metric']['Value']

    rain = r_rain['DailyForecasts'][0]['Day']['RainProbability']

    if check_bad_weather(int(temp), int(wind), int(rain)):
        result = 'Погода плохая!'
    else:
        result = 'Погода хорошая)'
    return temp, humidity, wind, rain, result

def check_loc(latitude, longitude):
    loc_key = find_loc_key(loc_url, f'{latitude},{longitude}')['Key']
    return check(loc_key)


def check_city(city):
    loc_key = find_loc_key(city_url, city)[0]['Key']
    return check(loc_key)


@app.route('/', methods=['POST', 'GET'])
def main():
    if request.method == 'POST':
        # latitude = request.form.get("latitude")
        # longitude = request.form.get("longitude")

        city1 = request.form.get('city1')
        temp1, humidity1, wind1, rain1, result1 = check_city(city1)

        city2 = request.form.get('city2')
        temp2, humidity2, wind2, rain2, result2 = check_city(city2)

        return (f'Город отправления: <br>'
                f'Температура: {temp1} С <br>'
                f'Влажность: {humidity1} % <br>'
                f'Скорость ветра: {wind1} км/ч <br>'
                f'Вероятность дождя: {rain1} % <br>'
                f'Результат: {result1}<br>'
                f'<br>'
                f'Город прибытия: <br>'
                f'Температура: {temp2} С <br>'
                f'Влажность: {humidity2} % <br>'
                f'Скорость ветра: {wind2} км/ч <br>'
                f'Вероятность дождя: {rain2} % <br>'
                f'Результат: {result2}')

    # return render_template('app.html')
    return render_template('app_city.html')

if __name__ == '__main__':
    app.run(host="127.0.0.1", port=5000, debug=True)
