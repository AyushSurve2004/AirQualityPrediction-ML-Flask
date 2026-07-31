# 🌍 Air Quality Prediction and Monitoring System

A Machine Learning-powered web application that predicts the Air Quality Index (AQI) based on air pollutant concentrations and provides users with real-time weather information, air quality categories, health recommendations, and interactive visualizations.

---

## 📌 Project Overview

The Air Quality Prediction and Monitoring System is designed to help users understand air pollution levels by predicting the Air Quality Index (AQI) using a trained Machine Learning model. The application also provides weather details, historical insights, and visual dashboards to support environmental awareness and decision-making.

---

## ✨ Features

- 🔐 User Registration and Login
- 🤖 Machine Learning-based AQI Prediction
- 📊 Interactive Dashboard with Charts
- 🌤️ Real-Time Weather Information
- 📈 Air Quality Trend Visualization
- 🚦 AQI Category Classification
- ❤️ Health Recommendations Based on AQI
- 📜 Prediction History
- 📱 Responsive Web Interface

---

## 🧠 Machine Learning

The prediction model is trained using historical air quality data collected from monitoring stations in India.

### Input Features

- PM2.5
- PM10
- NO₂
- SO₂
- CO

### Output

- Predicted AQI Value
- AQI Category
- Health Advisory

---

## 🛠️ Technologies Used

### Programming Language
- Python

### Framework
- Flask

### Machine Learning
- Scikit-learn
- Pandas
- NumPy
- Joblib

### Frontend
- HTML
- CSS
- Bootstrap 5
- JavaScript

### Database
- SQLite

### Data Visualization
- Chart.js

### APIs
- OpenWeather API

---

## 📂 Project Structure

```
AirQualityPrediction/
│
├── dataset/
├── models/
├── notebooks/
├── static/
│   ├── css/
│   ├── js/
│   └── images/
├── templates/
│   ├── index.html
│   ├── dashboard.html
│   ├── predict.html
│   ├── login.html
│   └── register.html
├── app.py
├── train_model.py
├── requirements.txt
├── README.md
└── .gitignore
```

---

## 🚀 Installation

### Clone the Repository

```bash
git clone https://github.com/your-username/air-quality-prediction.git
```

### Navigate to the Project Folder

```bash
cd air-quality-prediction
```

### Create a Virtual Environment

```bash
python -m venv venv
```

### Activate the Environment

**Windows**

```bash
venv\Scripts\activate
```

**Linux / macOS**

```bash
source venv/bin/activate
```

### Install Dependencies

```bash
pip install -r requirements.txt
```

### Run the Application

```bash
python app.py
```

---

## 📊 Dataset

The project uses historical air quality data containing pollutant measurements such as:

- PM2.5
- PM10
- NO
- NO₂
- NOx
- NH₃
- SO₂
- CO
- Ozone
- Benzene
- Toluene
- Xylene

The dataset is cleaned and preprocessed before training the Machine Learning model.

---

## 📈 Future Enhancements

- Live AQI data integration
- Multiple city support
- AQI forecasting using Time Series models
- Email alerts for unhealthy AQI levels
- Mobile application
- User profile and personalized history
- Deployment on AWS or Render

---

## 🎯 Learning Outcomes

This project helped me gain practical experience in:

- Machine Learning Model Development
- Data Cleaning and Preprocessing
- Flask Web Development
- REST API Integration
- Database Management
- Data Visualization
- User Authentication
- Model Deployment
- Full-Stack Python Development

---

## 📄 License

This project is developed for educational and learning purposes.

---

## 👨‍💻 Author

**Ayush Surve**

- MSc Computer Science
- Pune, Maharashtra, India
- LinkedIn: https://www.linkedin.com/in/ayush-surve-585484374/
- Email: ayushsurve94@gmail.com
