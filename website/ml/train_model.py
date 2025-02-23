import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
import joblib
import os
import gc

# Load dataset
dataset_path = os.path.join("dataset", "crop_yield.csv")  # Ensure this points to the correct location of your dataset
data = pd.read_csv(dataset_path)


# Update column names accordingly
data = data[['Region', 'Soil_Type', 'Temperature_Celsius', 'Weather_Condition', 'Crop']]  # Ensure column names match your data

# Drop rows with missing values
data.dropna(inplace=True)

# Create LabelEncoders for 'Region', 'Soil_Type', 'Weather_Condition', and 'Crop' columns
region_encoder = LabelEncoder()
soil_type_encoder = LabelEncoder()
weather_condition_encoder = LabelEncoder()
crop_encoder = LabelEncoder()

# Encode the categorical columns
data['Region'] = region_encoder.fit_transform(data['Region'])
data['Soil_Type'] = soil_type_encoder.fit_transform(data['Soil_Type'])
data['Weather_Condition'] = weather_condition_encoder.fit_transform(data['Weather_Condition'])
data['Crop'] = crop_encoder.fit_transform(data['Crop'])

# Define the feature set (X) and target variable (y)
X = data[['Region', 'Soil_Type', 'Temperature_Celsius', 'Weather_Condition']]  # Features
y = data['Crop']  # Target (Crop)

# Split the data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Reduce the number of estimators and limit features to reduce memory usage
model = RandomForestClassifier(n_estimators=10, max_features='sqrt', max_samples=0.8, random_state=42, n_jobs=-1)

# Train the RandomForest model
model.fit(X_train, y_train)

# Clear memory by invoking garbage collection
gc.collect()

# Save the trained model and encoders to disk
joblib.dump(model, 'website/ml/crop_prediction_model.pkl')
joblib.dump(region_encoder, 'website/ml/region_label_encoder.pkl')
joblib.dump(soil_type_encoder, 'website/ml/soil_type_label_encoder.pkl')
joblib.dump(weather_condition_encoder, 'website/ml/weather_condition_label_encoder.pkl')
joblib.dump(crop_encoder, 'website/ml/crop_label_encoder.pkl')

# Print a confirmation message
print("Model and encoders trained and saved successfully!")
