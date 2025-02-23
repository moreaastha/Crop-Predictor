class WeatherData:
    def __init__(self, region, soil_type, temperature, weather_condition):
        self.region = region
        self.soil_type = soil_type
        self.temperature = temperature
        self.weather_condition = weather_condition

    def get_region(self):
        return self.region

    def get_soil_type(self):
        return self.soil_type

    def get_temperature(self):
        return self.temperature

    def get_weather_condition(self):
        return self.weather_condition
