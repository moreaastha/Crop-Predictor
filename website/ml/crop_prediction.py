import joblib
import os
import numpy as np

class SimpleCropPrediction:
    def __init__(self):
        # Load the trained model and label encoders
        self.model = joblib.load(os.path.join("website", "ml", "crop_prediction_model.pkl"))
        self.le_region = joblib.load(os.path.join("website", "ml", "region_label_encoder.pkl"))
        self.le_soil = joblib.load(os.path.join("website", "ml", "soil_type_label_encoder.pkl"))
        self.le_weather = joblib.load(os.path.join("website", "ml", "weather_condition_label_encoder.pkl"))
        self.le_crop = joblib.load(os.path.join("website", "ml", "crop_label_encoder.pkl"))

    def predict(self, weather_data):
        # Create a feature array from the weather data
        region_encoded = self.le_region.transform([weather_data.get_region()])
        soil_encoded = self.le_soil.transform([weather_data.get_soil_type()])
        weather_encoded = self.le_weather.transform([weather_data.get_weather_condition()])
        temperature = weather_data.get_temperature()

        # Combine the features into an array
        features = np.array([[region_encoded[0], soil_encoded[0], temperature, weather_encoded[0]]])

        # Predict the crop index
        crop_index = self.model.predict(features)[0]

        # Convert the predicted index back to the crop name
        crop_name = self.le_crop.inverse_transform([crop_index])[0]
        return crop_name
    
    def predict_v2(self, weather_data):
        # Create a feature array from the weather data
        # region_encoded = self.le_region.transform([weather_data.get_region()])
        region_encoded = weather_data.get_region()
        # soil_encoded = self.le_soil.transform([weather_data.get_soil_type()])
        soil_encoded = weather_data.get_soil_type()
        # weather_encoded = self.le_weather.transform([weather_data.get_weather_condition()])
        weather_encoded = weather_data.get_weather_condition()
        temperature = weather_data.get_temperature()

        # Combine the features into an array
        features = np.array([[region_encoded, soil_encoded, temperature, weather_encoded]])

        # Predict the crop index
        crop_index = self.model.predict(features)[0]

        # Convert the predicted index back to the crop name
        crop_name = self.le_crop.inverse_transform([crop_index])[0]
        return crop_name
