from flask import Flask, render_template, request
import requests # type: ignore

app = Flask(__name__)

API_KEY = '8b7e5859fdf81a0554c49cbc45ef27f2'
BASE_URL = 'https://api.openweathermap.org/data/2.5/weather'


@app.route('/')
def index():
    city = 'Jakarta'
    weather_data = get_weather_data(city)
    return render_template('index.html', weather_data=weather_data)


@app.route('/search', methods=['GET', 'POST'])
def search():
    weather_data = None
    if request.method == 'POST':
        city = request.form.get('city', '').strip()
        if city:
            weather_data = get_weather_data(city)
    return render_template('search.html', weather_data=weather_data)


def get_weather_data(city):
    params = {
        'q': city,
        'appid': API_KEY,
        'units': 'metric',
        'lang': 'id'
    }
    try:
        response = requests.get(BASE_URL, params=params)
        response.raise_for_status()
        data = response.json()
        return {
            'city': data.get('name', 'Tidak diketahui'),
            'temperature': data['main'].get('temp', 'Tidak tersedia'),
            'description': 
                data['weather'][0].get('description', 'Tidak tersedia'),
            'icon': 
                f"https://openweathermap.org/img/wn/{data['weather'][0]['icon']}@2x.png"
        }
    except requests.exceptions.RequestException:
        return {'error': 'Gagal mengambil data cuaca. Coba lagi nanti.'}


if __name__ == '__main__':
    app.run(debug=True)