import telebot
import datetime
import Constants
from telebot import types
from datetime import date
from DataBaseHelper import DataBaseHelper
import WeatherParser
bot = telebot.TeleBot(Constants.BOT_TOKEN) # Initialise telegram bot.
db = DataBaseHelper("db.db") # Connect to database.


@bot.message_handler(commands=["start"])
def greetings(msg):
    """
    Method which is tell what should bot do after command start.
    Now, it write user_id and city to database.
    After this, method print various buttons for user, and send greetings message.
    """
    global db
    if (not db.user_exists(msg.from_user.id)):
        db.add_user((msg.from_user.id))
    else:
        Constants.CITY = db.get_user_city(msg.from_user.id) # If the user already exists, take he's city.
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True) # Buttons on user's messagebox.
    weather = types.KeyboardButton("☁️Weather")
    city = types.KeyboardButton("🏠Change home city")
    markup.add(weather, city) # Add buttons to markup

    bot.send_message(msg.chat.id,f"Welcome, <i>{msg.from_user.first_name}</i>!\n" + 
    f"My name is <b>{bot.get_me().first_name}</b> and my purpose to show the weather forecast.",
    parse_mode = "html")
    bot.send_message(msg.chat.id,f"For future work with this telegram bot, please choose an option", parse_mode = "html", reply_markup = markup)

@bot.message_handler(content_types = ["text"])
def respond(msg):
    """
    Method which give response to previous command.
    Now, it prints inline telegram buttons with different types of choise.
    """
    if msg.chat.type == "private":
        if msg.text == "☁️Weather":
            Constants.CITY = db.get_user_city(msg.from_user.id)

            markup = types.InlineKeyboardMarkup(row_width = 4) # Buttons under previous message.
            weather_now = types.InlineKeyboardButton("Now", callback_data="wnow")
            weather_today = types.InlineKeyboardButton("Today", callback_data="wtoday")
            weather_tomorrow = types.InlineKeyboardButton("Tomorrow", callback_data="wtomorrow")
            weather_week = types.InlineKeyboardButton("Week", callback_data="wweek")
            markup.add(weather_now, weather_today, weather_tomorrow, weather_week) # Add buttons to markup

            bot.send_message(msg.chat.id, "Choose the period", reply_markup=markup)
        elif msg.text == "🏠Change home city":  
            Constants.CITY = db.get_user_city(msg.from_user.id) # Take user's city from database.
            bot.send_message(msg.chat.id, f"Enter the city you want to know the weather for. Now it is: <b>{Constants.CITY}</b>", parse_mode="html")
            Constants.CHG_CITY = True # Option 'Change home city' was chosen.
        else:
            if Constants.CHG_CITY == True:
                Constants.CITY = msg.text
                Constants.CITY = Constants.CITY.replace('-',' ') # Remove dashes, because pyowm can't work with them.
                db.update_user(msg.from_user.id, Constants.CITY)

                bot.send_message(msg.chat.id, f"City was changed successfully! Now it is: <b>{Constants.CITY}</b>", parse_mode="html")
                Constants.CHG_CITY = False # Option 'Change home city' was executed.

@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
    """
    Method which is formulate response to inline buttons from previous method.
    Main logic of how bot works is here.
    Using flags which was added in previous method, determine which option was chosen.
    """
    try:
        if call.message:
            if call.data == 'wnow':
                wnow = WeatherParser.get_weather_for_now(Constants.CITY)
                temp = wnow.temperature("celsius")["temp"]
                temperature = "+" + str(temp) if temp >= 0 else "-" + str(temp)
                wind_speed = wnow.wind()["speed"]

                bot.send_message(call.message.chat.id, f"Now in <b>{Constants.CITY}</b> <i>{wnow.detailed_status}</i> " + 
                f"and temperature is <b>{temperature}</b> celsius." + 
                f" Speed of wind is <b>{wind_speed} m/s</b>, " + 
                f"humidity is <b>{wnow.humidity}%</b>, " + 
                f"clouds are <b>{wnow.clouds}</b>", parse_mode="html")
            elif call.data == "wtoday" or call.data == "wtomorrow" or call.data == "wweek":
                dat = date.today()
                dat_tomorrow = dat + datetime.timedelta(days=1)
                dat = str(dat)
                dat_tomorrow = str(dat_tomorrow)
                now = datetime.datetime.now()
                weat_msg = ""
                wtomorrow_daily = WeatherParser.get_weather_for_tomorrow(Constants.CITY)
                for item in wtomorrow_daily:
                    wdat = str(item["dt_txt"].split(' ')[0])
                    weather_time = WeatherParser.gettime_from_datetime(item["dt_txt"])
                    
                    if call.data == "wtoday" and wdat != dat:
                        continue
                    if call.data == "wtomorrow" and wdat != dat_tomorrow:
                        continue
                    if (weather_time == WeatherParser.gettime_from_datetime(now.replace(hour=6, minute=0, second=0, microsecond=0))
                    or weather_time == WeatherParser.gettime_from_datetime(now.replace(hour=15, minute=0, second=0, microsecond=0))
                    or weather_time == WeatherParser.gettime_from_datetime(now.replace(hour=21, minute=0, second=0, microsecond=0))):
                        weat_msg += WeatherParser.parser_helper(item, wdat, Constants.CITY)
                    
                bot.send_message(call.message.chat.id, weat_msg, parse_mode="html")
    except Exception as e:
        print(repr(e))

bot.polling(none_stop = True) # Launch bot.
        