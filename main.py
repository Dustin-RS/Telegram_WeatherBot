import telebot
import datetime
import Constants
from telebot import types
from datetime import date
from DataBaseHelper import DataBaseHelper
import WeatherParser
bot = telebot.TeleBot(Constants.BOT_TOKEN)  # Initialise telegram bot.
db = DataBaseHelper("db.db")  # Connect to database.


@bot.message_handler(commands=["start"])  # If the start command was activated.
def greetings(msg):
    """
    Method which is tell what should bot do after command start.
    Now, it write user_id and city to database.
    After this, method print various buttons for user, and send greetings message.
    """
    global db
    if not db.user_exists(msg.from_user.id):
        db.add_user(msg.from_user.id)
    else:
        Constants.CITY = db.get_user_city(msg.from_user.id)  # If the user already exists, take he's city.
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)  # Buttons on user's messagebox.
    weather = types.KeyboardButton("☁️Weather") 
    city = types.KeyboardButton("🏠Change home city")
    markup.add(weather, city)  # Add buttons to markup

    bot.send_message(msg.chat.id, f"Welcome, <i>{msg.from_user.first_name}</i>!\n" +
                                  f"My name is <b>{bot.get_me().first_name}</b> and my purpose to show "
                                  f"the weather forecast.", parse_mode="html")
    bot.send_message(msg.chat.id, f"For future work with this telegram bot, please choose an option", parse_mode="html",
                     reply_markup=markup)


@bot.message_handler(content_types=["text"])  # If user activated one of the options or typed smth. 
def respond(msg):
    """
    Method which give response to previous command.
    Now, it prints inline telegram buttons with different types of choice.
    """
    if msg.chat.type == "private":  # if the chat is personal(option in telegram).
        if msg.text == "☁️Weather":
            Constants.CITY = db.get_user_city(msg.from_user.id)  # Changing home city to value in database.

            markup = types.InlineKeyboardMarkup(row_width=4)  # Buttons under previous message.
            weather_now = types.InlineKeyboardButton("Now", callback_data="wnow")
            weather_today = types.InlineKeyboardButton("Today", callback_data="wtoday")
            weather_tomorrow = types.InlineKeyboardButton("Tomorrow", callback_data="wtomorrow")
            weather_week = types.InlineKeyboardButton("Week", callback_data="wweek")
            markup.add(weather_now, weather_today, weather_tomorrow, weather_week)  # Add buttons to markup

            bot.send_message(msg.chat.id, "Choose the period", reply_markup=markup)
        elif msg.text == "🏠Change home city":  
            Constants.CITY = db.get_user_city(msg.from_user.id)  # Take user's city from database.
            bot.send_message(msg.chat.id, f"Enter the city you want to know the weather for. "
                                          f"Now it is: <b>{Constants.CITY}</b>", parse_mode="html")
            Constants.CHG_CITY = True  # Option 'Change home city' was chosen.
        else:
            if Constants.CHG_CITY:
                Constants.CITY = msg.text  # Set to the city value new one from user's message text.
                Constants.CITY = Constants.CITY.replace('-', ' ')  # Remove dashes, because pyowm can't work with them.
                db.update_user(msg.from_user.id, Constants.CITY)  # Update user's home city.

                bot.send_message(msg.chat.id, f"City was changed successfully! Now it is: <b>{Constants.CITY}</b>",
                                 parse_mode="html")
                Constants.CHG_CITY = False  # Option 'Change home city' was executed.


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

                wnow = WeatherParser.get_weather_for_now(Constants.CITY)  # Get the current weather.
                temp = wnow.temperature("celsius")["temp"]  # Get the temperature from json file format.
                temperature = "+" + str(temp) if temp >= 0 else "-" + str(temp)  # Make temperature a
                # string with symbols '+' or '-'
                wind_speed = wnow.wind()["speed"] 
                desc = wnow.detailed_status  # Description of the weather outside, e.g.: rain.
                emoji_desc = WeatherParser.get_desc_emoji(desc)  # Emoji of the description.

                bot.send_message(call.message.chat.id, 
                                 f"Now in <b>{Constants.CITY}</b>:\n<i>{emoji_desc}{desc}</i>.\n" +
                                 f"🌡️Temperature is <b>{temperature}</b> celsius.\n" +
                                 f"💨Speed of wind is <b>{wind_speed} m/s</b>.\n" +
                                 f"💦Humidity is <b>{wnow.humidity}%</b>.\n" +
                                 f"☁️Clouds are <b>{wnow.clouds}</b>.\n",
                                 parse_mode="html")
            elif call.data == "wtoday" or call.data == "wtomorrow" or call.data == "wweek":
                dat = date.today()  # Take today date.
                dat_tomorrow = dat + datetime.timedelta(days=1)  # Take tomorrow's date from today's date.
                dat = str(dat)
                dat_tomorrow = str(dat_tomorrow)
                now = datetime.datetime.now()  # Take current date and time.
                weat_msg = ""  # Weather message. What will be printed in the end.
                # Take the data of the weather for future 5 days.
                wtomorrow_daily = WeatherParser.get_weather_for_tomorrow(Constants.CITY)
                for item in wtomorrow_daily:
                    wdat = str(item["dt_txt"].split(' ')[0])  # Take the date from datetime.
                    weather_time = WeatherParser.gettime_from_datetime(item["dt_txt"])  # Take time from datetime.
                    
                    if call.data == "wtoday" and wdat != dat:
                        continue
                    if call.data == "wtomorrow" and wdat != dat_tomorrow:
                        continue
                    if (weather_time == WeatherParser.gettime_from_datetime(now.replace(hour=6, minute=0, second=0,
                                                                                        microsecond=0))
                        or weather_time == WeatherParser.gettime_from_datetime(now.replace(hour=15, minute=0, second=0,
                                                                                           microsecond=0))
                        or weather_time == WeatherParser.gettime_from_datetime(now.replace(hour=21, minute=0, second=0,
                                                                                           microsecond=0))):
                        weat_msg += WeatherParser.parser_helper(item, wdat, Constants.CITY)
                    
                bot.send_message(call.message.chat.id, weat_msg, parse_mode="html")
    except Exception as e:
        print(repr(e))


bot.polling(none_stop=True)  # Launch bot.
