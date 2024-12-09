import requests
from flask import Flask, render_template, request

app = Flask(__name__)

api_url = 'https://dataservice.accuweather.com/'
api_key = 'KRAgAGp4i6q2g5ZnNHkYO8CKWEYLLbNY'
loc_url = 'locations/v1/cities/geoposition/search'
city_url = '/locations/v1/cities/search'

def find_loc_key(url, data):
    loc_key = requests.get(api_url + url,
                           params={
                               'q': data,
                               'apikey': api_key
                           }).json()
    print(loc_key)
    return loc_key

def check_bad_weather(temp, wind, rain):
    if 0 <= temp <= 35 and wind <= 50 and rain <= 70:
        return False
    return True


@app.route('/', methods=['POST', 'GET'])
def main():
    if request.method == 'POST':
        # latitude = request.form.get("latitude")
        # longitude = request.form.get("longitude")
        # loc_key = find_loc_key(loc_url, f'{latitude},{longitude}')['Key']

        city = request.form.get('city')
        loc_key = find_loc_key(city_url, city)[0]['Key']

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

        return (f'Результаты: <br>'
                f'Температура: {temp} С <br>'
                f'Влажность: {humidity} % <br>'
                f'Скорость ветра: {wind} км/ч <br>'
                f'Вероятность дождя: {rain} % <br>'
                f'Результат: {result}')

    # return render_template('app.html')
    return render_template('app_city.html')

if __name__ == '__main__':
    app.run(host="127.0.0.1", port=5000, debug=True)
