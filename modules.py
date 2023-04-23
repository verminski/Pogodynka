import datetime
import requests
import geocoder
from ast import literal_eval

class WeatherForecast:
    def __init__(self):
        try:
            with open("weather_data.txt", "r") as file:
                self.weather_data = literal_eval(file.read())
        except FileNotFoundError:
            self.weather_data = {}

    def __setitem__(self, key, forecast):
        city, date = key
        if city not in self.weather_data:
            self.weather_data[city] = {}
        self.weather_data[city][date] = forecast
        with open("weather_data.txt", "w") as file:
            file.write(str(self.weather_data))

    def __getitem__(self, key):
        city, date = key
        return self.weather_data[city][date]

    def __iter__(self):
        return iter(self.weather_data)

    def items(self):

        # result = []
        # for city in self.weather_data:
        #     for date in self.weather_data[city]:
        #         result.append((city, date, self.weather_data[city][date]))
        # return result

        return ((city, date, self.weather_data[city][date]) for city in self.weather_data for date in self.weather_data[city])

    def fetch_forecast(self, city, latitude, longitude, forecast_date):
        if city in self.weather_data and forecast_date in self.weather_data[city]:
            print(f"Forecast for {city} on {forecast_date} already exists, cached data will be displayed.")
            return self.weather_data[city][forecast_date]

        print(f"Forecast for this date does not exist, new data will be downloaded")
        url =f"https://api.open-meteo.com/v1/forecast?latitude={latitude}&longitude={longitude}&daily=precipitation_sum&timezone=Europe%2FLondon&start_date={forecast_date}&end_date={forecast_date}"
        forecast_response = requests.get(url)

        if forecast_response.status_code == 200:
            print("Forecast downloaded successfully!")
            self[city, forecast_date] = forecast_response.json()
            return forecast_response.json()
        else:
            print("Error while downloading forecast")
            exit()

def get_location(location):
    if location == "":
        print("Nie podano lokalizacji. Kończę program.")
        exit()

    try:
        g = geocoder.osm(location)
        latitude = g.latlng[0]
        longitude = g.latlng[1]
        return latitude, longitude
    except:
        print("Brak takiej lokalizacji")
        return None, None

def get_forecast_date(forecast_date):
    try:
        if forecast_date == "":
            print("No date. Checking weather for the next day..")
            forecast_date = datetime.datetime.today() + datetime.timedelta(days=1)
            forecast_date = forecast_date.strftime("%Y-%m-%d")
        else:
            forecast_date = datetime.datetime.strptime(forecast_date, "%Y-%m-%d")
            forecast_date = forecast_date.strftime("%Y-%m-%d")
    except ValueError:
        print("Wrong date! Exiting program!")
        exit()

    return forecast_date

def check_rain(forecast_data):
    forecast_data = float(forecast_data["daily"]["precipitation_sum"][0])
    if forecast_data == 0.0:
        print("It won't rain.")
    elif forecast_data < 0.0:
        print("I have no idea.")
    else:
        print(f"It will rain: {forecast_data} mm.")

# def get_forecast(latitude, longitude, location, forecast_date):
#     try:
#         with open("weather_data.txt", "r") as file:
#             weather_data = file.read()
#             weather_data = literal_eval(weather_data)
#     except FileNotFoundError:
#         weather_data = {}
#
#     if forecast_date in weather_data:
#         if location in weather_data[forecast_date]:
#             print(f"Prognoza dla {location} na dzień {forecast_date} jest zczytana z pliku.")
#             return weather_data[forecast_date][location]
#
#     url =f"https://api.open-meteo.com/v1/forecast?latitude={latitude}&longitude={longitude}&daily=precipitation_sum&timezone=Europe%2FLondon&start_date={forecast_date}&end_date={forecast_date}"
#     forecast_response = requests.get(url)
#
#     if forecast_response.status_code == 200:
#         print("Prognoza pobrana z Open-Meteo")
#         weather_data[forecast_date] = {}
#         weather_data[forecast_date][location] = forecast_response.json()
#     else:
#         print("Problem z pobraniem prognozy.")
#         exit()
#
#     with open("weather_data.txt", "w") as file:
#         file.write(str(weather_data))
#
#     return forecast_response.json()

