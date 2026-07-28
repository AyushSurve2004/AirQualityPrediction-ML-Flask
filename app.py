from realtime_aqi import get_realtime_aqi
import requests
import datetime
API_KEY = "d84a0c9767593157dfe39e0e93f266fb"
from flask import Flask, render_template, request, redirect, url_for, session
from functools import wraps
import pandas as pd
import numpy as np
import joblib
import sqlite3

app = Flask(__name__)

def get_aqi_category(aqi):
    if aqi <= 50:
        return "Good"
    elif aqi <= 100:
        return "Moderate"
    elif aqi <= 200:
        return "Poor"
    elif aqi <= 300:
        return "Very Poor"
    else:
        return "Severe"

def get_health_advice(aqi):
    if aqi <= 50:
        return "Air quality is good. Enjoy outdoor activities."
    elif aqi <= 100:
        return "Air quality is acceptable. Sensitive people should take care."
    elif aqi <= 200:
        return "Sensitive groups should reduce prolonged outdoor activities."
    elif aqi <= 300:
        return "Avoid outdoor activities if possible. Health effects may occur."
    else:
        return "Avoid outdoor activities. Air quality is hazardous."


@app.route("/")
def home():
    return render_template("index.html")

app.secret_key = "aqi_secret_key_2026"

def login_required(f):

    @wraps(f)
    def decorated_function(*args, **kwargs):

        if "username" not in session:
            return redirect("/login")

        return f(*args, **kwargs)

    return decorated_function

def init_db():

    conn = sqlite3.connect("database.db")

    cursor = conn.cursor()


    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users(

            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE,
            password TEXT

        )
    """)


    cursor.execute("""
        CREATE TABLE IF NOT EXISTS predictions(

            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT,
            date TEXT,
            pm25 REAL,
            pm10 REAL,
            no2 REAL,
            co REAL,
            so2 REAL,
            aqi REAL,
            status TEXT

        )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS realtime_aqi(

        id INTEGER PRIMARY KEY AUTOINCREMENT,
        city TEXT,
        date TEXT,
        aqi REAL,
        category TEXT

    )
""")


    conn.commit()

    conn.close()


init_db()


# Load trained model
model = joblib.load("models/aqi_prediction_model.pkl")

@app.route("/download")
@login_required
def download():

    from flask import send_file

    return send_file(
        "predictions.csv",
        as_attachment=True
    )

@app.route('/realtime', methods=['GET','POST'])
@login_required
def realtime():

    data = None

    if request.method == 'POST':
        city = request.form['city']
        data = get_realtime_aqi(city)

        if data:
            data["category"] = get_aqi_category(data["aqi"])
            data["advice"] = get_health_advice(data["aqi"])

            conn = sqlite3.connect("database.db")
            cursor = conn.cursor()

            cursor.execute(
                """
                INSERT INTO realtime_aqi
                (city, date, aqi, category)
                VALUES(?,?,?,?)
                """,
                (
                    data["city"],
                    str(datetime.datetime.now()),
                    data["aqi"],
                    data["category"]
                )
            )

            conn.commit()
            conn.close()

    return render_template('realtime.html', data=data)
@app.route("/predict", methods=["GET", "POST"])
@login_required
def predict():

    if request.method == "GET":
        return render_template("predict.html")

    try:

        pm25 = float(request.form["PM2.5"])
        pm10 = float(request.form["PM10"])
        no2 = float(request.form["NO2"])
        co = float(request.form["CO"])
        so2 = float(request.form["SO2"])


        input_data = pd.DataFrame(
            [[pm25, pm10, 0, no2, 0, 0, co, so2, 0, 0, 0, 0]],
            columns=[
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
        )


        prediction = model.predict(input_data)[0]


        if prediction <= 50:
            status = "Good"

        elif prediction <= 100:
            status = "Moderate"

        elif prediction <= 200:
            status = "Poor"

        else:
            status = "Severe"


        history = pd.DataFrame(
            [[
                datetime.datetime.now(),
                pm25,
                pm10,
                no2,
                co,
                so2,
                round(prediction,2),
                status
            ]],
            columns=[
                "Date",
                "PM2.5",
                "PM10",
                "NO2",
                "CO",
                "SO2",
                "AQI",
                "Status"
            ]
        )


        history.to_csv(
            "predictions.csv",
            mode="a",
            header=False,
            index=False
        )


        conn = sqlite3.connect("database.db")
        cursor = conn.cursor()

        cursor.execute(
            """
            INSERT INTO predictions
            (username,date,pm25,pm10,no2,co,so2,aqi,status)
            VALUES(?,?,?,?,?,?,?,?,?)
            """,
            (
                session["username"],
                str(datetime.datetime.now()),
                pm25,
                pm10,
                no2,
                co,
                so2,
                round(prediction,2),
                status
            )
        )

        conn.commit()
        conn.close()


        return render_template(
            "result.html",
            prediction=round(prediction,2),
            status=status
        )


    except Exception as e:

        return str(e)

@app.route("/dashboard")
@login_required
def dashboard():

    # ---------------- MODEL PERFORMANCE ----------------
    model_name = "Random Forest Regressor"
    r2_score = 0.94
    rmse = 8.52
    mae = 6.11

    # ---------------- LOAD DATASET ----------------
    data = pd.read_csv("dataset/cleaned_air_quality.csv")

    cities = sorted(data["City"].unique().tolist())
    selected_city = request.args.get("city")

    if selected_city:
        city_data = data[data["City"] == selected_city]
    else:
        city_data = data

    # ---------------- AQI TREND ----------------
    latest_data = city_data.tail(7)

    dates = latest_data["Date"].astype(str).tolist()
    aqi_values = latest_data["AQI"].astype(float).tolist()

    # ---------------- DASHBOARD CARDS ----------------
    #avg_aqi = round(city_data["AQI"].mean(), 2)
    max_aqi = round(city_data["AQI"].max(), 2)
    min_aqi = round(city_data["AQI"].min(), 2)
    total_records = len(city_data)

    # ---------------- POLLUTION VALUES ----------------
    pm25 = round(city_data["PM2.5"].mean(), 2)
    pm10 = round(city_data["PM10"].mean(), 2)
    no2 = round(city_data["NO2"].mean(), 2)
    co = round(city_data["CO"].mean(), 2)
    so2 = round(city_data["SO2"].mean(), 2)

    # ---------------- WEATHER ----------------
    city_name = selected_city if selected_city else "Delhi"

    weather_url = f"https://api.openweathermap.org/data/2.5/weather?q={city_name}&appid={API_KEY}&units=metric"

    # Get latitude & longitude
    geo_url = (
        f"https://api.openweathermap.org/geo/1.0/direct"
        f"?q={city_name}&limit=1&appid={API_KEY}"
    )

    geo_response = requests.get(geo_url)
    geo_data = geo_response.json()

    if geo_data:
        lat = geo_data[0]["lat"]
        lon = geo_data[0]["lon"]
    else:
        lat = 28.6139
        lon = 77.2090

    # Live Air Pollution
    air_url = (
        f"https://api.openweathermap.org/data/2.5/air_pollution"
        f"?lat={lat}&lon={lon}&appid={API_KEY}"
    )

    air_response = requests.get(air_url)
    air_data = air_response.json()

    try:
        weather_response = requests.get(weather_url)
        weather = weather_response.json()

        if "main" in weather:
            temperature = weather["main"]["temp"]
            humidity = weather["main"]["humidity"]
            wind = weather["wind"]["speed"]
            description = weather["weather"][0]["description"]
        else:
            temperature = "N/A"
            humidity = "N/A"
            wind = "N/A"
            description = "Unavailable"

        # Live Pollution Values
        components = air_data["list"][0]["components"]

        live_pm25 = components.get("pm2_5", 0)
        live_pm10 = components.get("pm10", 0)
        live_no2 = components.get("no2", 0)
        live_co = components.get("co", 0)
        live_so2 = components.get("so2", 0)

        input_data = pd.DataFrame(
            [[
                live_pm25,
                live_pm10,
                0,
                live_no2,
                0,
                0,
                live_co,
                live_so2,
                0,
                0,
                0,
                0
            ]],
            columns=[
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
        )

        predicted_aqi = model.predict(input_data)[0]
        avg_aqi = round(predicted_aqi, 2)


        print("Live PM2.5:", live_pm25)
        print("Live PM10 :", live_pm10)
        print("Live NO2  :", live_no2)
        print("Live CO   :", live_co)
        print("Live SO2  :", live_so2)

    except:
        temperature = "N/A"
        humidity = "N/A"
        wind = "N/A"
        description = "Unavailable"

        live_pm25 = 0
        live_pm10 = 0
        live_no2 = 0
        live_co = 0
        live_so2 = 0

    # ---------------- PREDICTION HISTORY ----------------
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()

    cursor.execute("""
        SELECT date, pm25, pm10, no2, co, so2, aqi, status
        FROM predictions
        WHERE username=?
        ORDER BY id DESC
        LIMIT 10
    """, (session["username"],))

    rows = cursor.fetchall()
    print("ROWS =", rows)
    conn.close()

    history_data = []
    prediction_dates = []
    prediction_values = []

    for row in rows:
        history_data.append({
            "Date": row[0],
            "PM2.5": row[1],
            "PM10": row[2],
            "NO2": row[3],
            "CO": row[4],
            "SO2": row[5],
            "AQI": row[6],
            "Status": row[7]
        })

        prediction_dates.append(row[0])
        prediction_values.append(row[6])

    return render_template(
        "dashboard.html",
        cities=cities,
        avg_aqi=avg_aqi,
        max_aqi=max_aqi,
        min_aqi=min_aqi,
        total_records=total_records,
        dates=dates,
        aqi_values=aqi_values,
        pm25=live_pm25,
        pm10=live_pm10,
        no2=live_no2,
        co=live_co,
        so2=live_so2,
        temperature=temperature,
        humidity=humidity,
        wind=wind,
        description=description,
        history_data=history_data,
        prediction_dates=prediction_dates,
        prediction_values=prediction_values,
        model_name=model_name,
        r2_score=r2_score,
        rmse=rmse,
        mae=mae
    )

@app.route("/my_predictions")
@login_required
def my_predictions():

    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()

    cursor.execute("""
        SELECT date, pm25, pm10, no2, co, so2, aqi, status
        FROM predictions
        WHERE username=?
        ORDER BY id DESC
    """, (session["username"],))

    predictions = cursor.fetchall()
    conn.close()

    return render_template(
        "my_predictions.html",
        predictions=predictions
    )

@app.route("/realtime_history")
@login_required
def realtime_history():

    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()

    cursor.execute("""
        SELECT city, date, aqi, category
        FROM realtime_aqi
        ORDER BY id DESC
    """)

    history = cursor.fetchall()

    conn.close()

    return render_template(
        "realtime_history.html",
        history=history
    )


@app.route("/history")
@login_required
def history():

    try:
        data = pd.read_csv("predictions.csv")

        return render_template(
            "history.html",
            tables=data.to_dict(orient="records")
        )

    except Exception:
        return "No prediction history available"


@app.route("/register", methods=["GET", "POST"])
def register():

    if request.method == "POST":

        username = request.form["username"]
        password = request.form["password"]

        conn = sqlite3.connect("database.db")
        cursor = conn.cursor()

        try:
            cursor.execute(
                "INSERT INTO users(username,password) VALUES(?,?)",
                (username, password)
            )

            conn.commit()
            return redirect("/login")

        except:
            return "Username already exists"

        finally:
            conn.close()

    return render_template("register.html")


@app.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":

        username = request.form["username"]
        password = request.form["password"]

        conn = sqlite3.connect("database.db")
        cursor = conn.cursor()

        cursor.execute(
            "SELECT * FROM users WHERE username=? AND password=?",
            (username, password)
        )

        user = cursor.fetchone()
        conn.close()

        if user:
            session["username"] = username
            return redirect("/dashboard")

        return "Invalid Username or Password"

    return render_template("login.html")


@app.route("/logout")
def logout():

    session.pop("username", None)
    return redirect("/")



if __name__ == "__main__":
    app.run(debug=True)