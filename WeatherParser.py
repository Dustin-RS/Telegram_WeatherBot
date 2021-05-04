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
    clouds = wtomorrow["clouds"]["all"]
    wind_speed = wtomorrow["wind"]["speed"]
    time = str(item["dt_txt"].split(' ')[1])
    time = time[:-3]
    wdat = wdat.replace('-', '/')

    tmp = f"On {wdat} at {time}" + f" in <b>{CITY}</b> <i>{desc}</i> " + f"and temperature is <b>{temperature}</b> celsius." + f" Speed of wind is <b>{wind_speed} m/s</b>, " + f"humidity is <b>{humidity}%</b>, " + f"clouds are <b>{clouds}</b>\n"
    return tmp
def gettime_from_datetime(temp_time):
    """
    Take time from datetime type.
    """
    return datetime.datetime.strptime(str(temp_time), "%Y-%m-%d %H:%M:%S").strftime('%H:%M:%S')