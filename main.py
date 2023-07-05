from modules import get_location, get_forecast_date, WeatherForecast, check_rain

option = input("Which command would you like to execute? (list, new, manual, saved, cities, exit): ")
while option != "exit":
    weather_forecast = WeatherForecast()
    if option == "list":
        print("All saved forecasts data")
        for city, data, forecast in weather_forecast.items():
            print(f"{city} on {data}: {forecast}")
            check_rain(forecast)

    elif option == "new":
        try:
            city = input("Enter the city name: ")
            date = input("Enter the date of the forecast (YYYY-MM-DD): ")
            date = get_forecast_date(date)
            latitude, longitude = get_location(city)
            forecast_data = weather_forecast.fetch_forecast(city, latitude, longitude, date)
            check_rain(forecast_data)
        except:
            print("Error! Wrong input!")

    elif option == "manual":
        try:
            city = input("Enter the city name: ")
            date = input("Enter the date of the forecast (YYYY-MM-DD): ")
            precipitation = input("Enter precipitation value: ")
            weather_forecast[city, date] = {"daily": {"precipitation_sum": [float(precipitation)]}}
        except:
            print("Error! Wrong input!")

    elif option == "saved":
        try:
            city = input("Enter the city name: ")
            date = input("Enter the date of the forecast (YYYY-MM-DD): ")
            forecast = weather_forecast[city, date]
            print(f"{city} forecast for {date}: {forecast}")
            check_rain(forecast)
        except:
            print("Error, wrong input!")

    elif option == "cities":
        try:
            for city in weather_forecast:
                print(city)
        except:
            print("Error, wrong input!")

    option = input("Which command would you like to execute? (list, new, manual, saved, cities, exit): ")