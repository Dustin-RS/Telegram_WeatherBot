import pyowm
OWM = pyowm.OWM("ff8358314800130efdd64202906f389f")
mgr = OWM.weather_manager()


def get_weather_for_now(city):
    observation = mgr.weather_at_place(city)
    wnow = observation.weather
    return wnow