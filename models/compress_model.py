import joblib

model = joblib.load("models/aqi_prediction_model.pkl")

joblib.dump(
    model,
    "models/aqi_prediction_model_compressed.pkl",
    compress=9
)

print("Compression completed")