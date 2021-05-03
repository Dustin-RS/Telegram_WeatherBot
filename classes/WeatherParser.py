import pyowm
from pyowm.utils import timestamps
OWM = pyowm.OWM("ff8358314800130efdd64202906f389f")
mgr = OWM.weather_manager()


def get_weather_for_now(city):
    observation = mgr.weather_at_place(city)
    wnow = observation.weather
    return wnow
def get_weather_for_tomorrow(city):
    daily_forecaster = mgr.forecast_at_place(city, 'daily')
    tomorrow = timestamps.tomorrow()
    wtomorrow = daily_forecaster.get_weather_at(tomorrow) 
    return wtomorrow