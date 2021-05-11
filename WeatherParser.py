import json
import pyowm
import datetime
import requests
import Constants
OWM = pyowm.OWM(Constants.WEATHER_TOKEN)  # Create OpenWeatherMap object.
mgr = OWM.weather_manager()  # Create manager for working with owm object.


def get_weather_for_now(city):
    """
    Take current weather.
    """
    observation = mgr.weather_at_place(city)  # Get the current weather in the city.
    wnow = observation.weather
    return wnow


def get_weather_for_tomorrow(city):
    """
    Take weather forecast for next 5 days, including today.
    """
    # json file link on future forecast.
    url = f"http://api.openweathermap.org/data/2.5/forecast?q={city}&appid={Constants.WEATHER_TOKEN}"
    r = requests.get(url)  # Get the json file.
    data = json.loads(r.text)  # Load it.
    tenki_nextday = data["list"]  # Get the whole data list.
    return tenki_nextday


def get_desc_emoji(desc):
    """
    Set appropriate emoji to weather description.
    """
    emoji_desc = ''
    if desc == "clear sky":
        emoji_desc = '🔵'  # Blue sky emoji.
    elif desc.find("clouds") != -1:
        emoji_desc = '☁️'  # Cloud emoji.
    elif desc.find("rain") != -1:
        emoji_desc = '🌦️'  # Rain cloud emoji.
    elif desc.find("thunderstorm") != -1:
        emoji_desc = '🌩️'  # Thunderstorm cloud emoji.
    elif desc.find("snow") != -1:
        emoji_desc = '❄️'  # Snow emoji.
    elif (desc == "mist" or desc == "Smoke"
          or desc == "Haze" or desc == "fog"
          or desc == "sand" or desc == "dust"):
        emoji_desc = '🌫️'  # Fog cloud emoji.
    return emoji_desc


def parser_helper(item, wdat, city):
    """
    Takes all necessary info from json file and make it more beautiful.
    """
    wtomorrow = item
    # On json file temperature was set by kelvin. By this action we change it to celsius.
    temp = wtomorrow["main"]["temp"] - Constants.FROM_KELVIN_TO_CELSIUS
    temp = round(temp, 2)  # Round float value to two digits after point.
    temperature = "+" + str(temp) if temp >= 0 else "-" + str(temp)
    humidity = wtomorrow["main"]["humidity"]
    desc = wtomorrow["weather"][0]["description"]
    clouds = wtomorrow["clouds"]["all"]
    wind_speed = wtomorrow["wind"]["speed"]
    time = str(item["dt_txt"].split(' ')[1])
    time = time[:-3]
    wdat = wdat.replace('-', '/')
    emoji_desc = get_desc_emoji(desc)

    tmp = f"On <b><i>{wdat}</i></b> at <b>{time}</b>"
    tmp += f" in <b>{city}</b>:\n<i>{emoji_desc}{desc}</i>.\n"
    tmp += f"🌡️Temperature is <b>{temperature}</b> celsius.\n"
    tmp += f"💨Speed of wind is <b>{wind_speed} m/s</b>.\n"
    tmp += f"💦Humidity is <b>{humidity}%</b>.\n"
    tmp += f"☁️Clouds are <b>{clouds}</b>.\n"
    return tmp


def gettime_from_datetime(temp_time):
    """
    Take time from datetime type.
    """
    return datetime.datetime.strptime(str(temp_time), "%Y-%m-%d %H:%M:%S").strftime('%H:%M:%S')
