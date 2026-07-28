import requests

WAQI_TOKEN = "d3e3a16417d425516a9b9b1fc5c9f8e94eed5349"

def get_realtime_aqi(city):
    url = f"https://api.waqi.info/feed/{city}/?token={WAQI_TOKEN}"

    response = requests.get(url)
    data = response.json()

    if data["status"] == "ok":
        aqi_data = data["data"]

        result = {
            "aqi": aqi_data.get("aqi"),
            "city": aqi_data["city"]["name"],
            "pm25": aqi_data["iaqi"].get("pm25", {}).get("v"),
            "pm10": aqi_data["iaqi"].get("pm10", {}).get("v"),
            "no2": aqi_data["iaqi"].get("no2", {}).get("v"),
            "so2": aqi_data["iaqi"].get("so2", {}).get("v"),
            "co": aqi_data["iaqi"].get("co", {}).get("v")
        }

        return result

    else:
        return None