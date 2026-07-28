import pandas as pd

from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, r2_score

import joblib


# Load cleaned dataset
data = pd.read_csv("dataset/cleaned_air_quality.csv")


print("Dataset Loaded")
print(data.head())


# Select features
features = [
    "PM2.5",
    "PM10",
    "NO",
    "NO2",
    "NOx",
    "NH3",
    "CO",
    "SO2",
    "O3",
    "Benzene",
    "Toluene",
    "Xylene"
]


X = data[features]

# Target variable
y = data["AQI"]


# Split data
X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42
)


print("Training data:", X_train.shape)
print("Testing data:", X_test.shape)


# Create model
model = RandomForestRegressor(
    n_estimators=100,
    random_state=42
)


# Train model
print("Training model...")

model.fit(X_train, y_train)


# Prediction
prediction = model.predict(X_test)


# Evaluation

mae = mean_absolute_error(y_test, prediction)
r2 = r2_score(y_test, prediction)


print("\nModel Performance")
print("----------------------")
print("MAE:", mae)
print("R2 Score:", r2)


# Save model

joblib.dump(
    model,
    "models/aqi_prediction_model.pkl"
)


print("\nModel saved successfully!")