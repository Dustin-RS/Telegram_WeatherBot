import json
import pyowm
import requests
import datetime
import sys
sys.path.append("..") 
import Constants
from pyowm.utils import timestamps
from datetime import date
OWM = pyowm.OWM(Constants.WEATHER_TOKEN) # Create OpenWeatherMap object.
mgr = OWM.weather_manager() # Create manager for working with owm object.


def get_weather_for_now(city):
    """
    Take current weather.
    """
    observation = mgr.weather_at_place(city)
    wnow = observation.weather
    return wnow
def get_weather_for_tomorrow(city):
    """
    Take weather forecast for next 5 days, including today.
    """
    url = f"http://api.openweathermap.org/data/2.5/forecast?q={city}&appid={Constants.WEATHER_TOKEN}"
    r = requests.get(url)
    data = json.loads(r.text)
    tenki_nextday = data["list"]
    return tenki_nextday
def parser_helper(item, wdat, CITY):
    """
    Takes all necessary info from json file and make it more beautiful.
    """
    wtomorrow = item
    temp = wtomorrow["main"]["temp"] - Constants.FROM_KELVIN_TO_CELSIUS
    temp = round(temp,2)
    temperature = "+" + str(temp) if temp >= 0 else "-" + str(temp)
    humidity = wtomorrow["main"]["humidity"]
    desc = wtomorrow["weather"][0]["description"]
    emoj_desc = ''
    clouds = wtomorrow["clouds"]["all"]
    wind_speed = wtomorrow["wind"]["speed"]
    time = str(item["dt_txt"].split(' ')[1])
    time = time[:-3]
    wdat = wdat.replace('-', '/')

    if desc == "clear sky":
        emoj_desc = '🔵'
    elif desc.find("clouds") != -1:
        emoji_desc = '☁️'
    elif desc.find("rain") != -1:
        emoji_desc = '🌦️'
    elif desc.find("thunderstorm") != -1:
        emoji_desc = '🌩️'
    elif desc.find("snow") != -1:
        emoji_desc = '❄️'
    elif (desc == "mist" or desc == "Smoke" 
        or desc == "Haze" or desc == "fog"
        or desc == "sand" or desc == "dust"):
        emoji_desc = '🌫️'
    tmp = f"On <b><i>{wdat}</i></b> at <b>{time}</b>"
    tmp += f" in <b>{CITY}</b>:\n<i>{emoji_desc}{desc}</i>.\n" 
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