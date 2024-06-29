from flask import Flask, render_template, request
import requests
import json
import os

app = Flask(__name__)

# openweathermap api key
api_key = 'd94ec4df6e51870324d0daf2d3e8007e'

# fetch weather data ####
# get geo data from zipcode
def get_geolocation(zipcode, api_key):
    base_url = 'https://api.openweathermap.org/geo/1.0/zip'
    params = {
        'zip': zipcode,
        'appid': api_key
    }
    response = requests.get(base_url, params=params)
    if response.status_code == 200:
        data = response.json()
        lat = data.get('lat')
        lon = data.get('lon')
        return lat, lon
    else:
        print('Error:', response.status_code, response.text)
        return None

#get weather data from geodata
def fetch_weather_data(lat, lon, api_key):
    api_url = f'https://api.openweathermap.org/data/3.0/onecall?lat={lat}&lon={lon}&appid={api_key}&units=imperial'
    response = requests.get(api_url)
    if response.status_code == 200:
        data = response.json()
        return data
    else:
        print("Failed to fetch data:", response.status_code)
        return None

# Save weather data to a file
def save_weather_data(data):
    os.makedirs('data', exist_ok=True) 
    with open('data/weather_data.json', 'w') as f:
        json.dump(data, f, indent=4)

# Load weather data from a file
def load_weather_data():
    if not os.path.exists('data/weather_data.json'):
        print("File not found. Fetching new data.")
        return None
    with open('data/weather_data.json', 'r') as f:
        data = json.load(f)
    return data
    
@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        zipcode = request.form['zipcode']
        lat, lon = get_geolocation(zipcode, api_key)
        if lat is not None and lon is not None:
            data = fetch_weather_data(lat, lon, api_key)
        else:
            data = None
    else:
        data = load_weather_data()
    
    if data is None:
        print("No weather data available.")
    
    # Print data for debugging purposes
    print(data)
    
    return render_template('hello.html', weather=data)

if __name__ == '__main__':
    app.run()
