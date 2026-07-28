import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd

# Load dataset
data = pd.read_csv("dataset/cleaned_air_quality.csv")

print("========== FIRST 5 ROWS ==========")
print(data.head())

print("\n========== COLUMN NAMES ==========")
print(list(data.columns))

print("\n========== DATASET INFORMATION ==========")
print(data.info())

print("\n========== MISSING VALUES ==========")
print(data.isnull().sum())

print("\n========== DUPLICATE ROWS ==========")
print(data.duplicated().sum())

data = data.drop_duplicates()

print("\nDuplicate rows removed successfully!")

# Remove rows where AQI is missing
data = data.dropna(subset=["AQI"])

print("\nRows after removing missing AQI:", len(data))

# Fill missing values in numeric columns using the median
numeric_columns = [
    "PM2.5", "PM10", "NO", "NO2", "NOx",
    "NH3", "CO", "SO2", "O3",
    "Benzene", "Toluene", "Xylene"
]

for column in numeric_columns:
    data[column] = data[column].fillna(data[column].median())

print("\nMissing values in feature columns filled successfully!")

print("\n========== MISSING VALUES AFTER CLEANING ==========")
print(data.isnull().sum())

# Save cleaned dataset
data.to_csv("dataset/cleaned_air_quality.csv", index=False)

print("\nCleaned dataset saved successfully!")

import os

print("\nCurrent Working Directory:")
print(os.getcwd())

print("\nFiles in dataset folder:")
print(os.listdir("dataset"))

print("\n========== SUMMARY STATISTICS ==========")
print(data.describe())

#plt.figure(figsize=(10, 6))
#plt.hist(data["AQI"], bins=30)

#plt.title("Distribution of AQI")
#plt.xlabel("AQI")
#plt.ylabel("Frequency")

#plt.show()

# Correlation Heatmap

plt.figure(figsize=(12, 8))

correlation = data.corr(numeric_only=True)

sns.heatmap(correlation,
            annot=True,
            cmap="coolwarm",
            fmt=".2f")

plt.title("Correlation Heatmap")

plt.show()