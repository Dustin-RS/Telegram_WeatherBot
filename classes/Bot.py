import telebot
from telebot import types
import classes.WeatherParser as WeatherParser
TOKEN = '1695565688:AAGW95Q4N0MXGC1E-sscQ171dNa_dII1aiY' # bot token from @BotFather
bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=['start'])
def greetings(msg):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    weather = types.KeyboardButton("☁️Weather")
    city = types.KeyboardButton("🏠Change home city")

    markup.add(weather, city)

    bot.send_message(msg.chat.id,f"Welcome, <i>{msg.from_user.first_name}</i>!\nMy name is <b>{bot.get_me().first_name}</b> and my purpose to show the weather forecast.",
    parse_mode = "html")
    bot.send_message(msg.chat.id,f"For future work with this telegram bot, please choose an option", parse_mode = "html", reply_markup = markup)

@bot.message_handler(content_types = ["text"])
def respond(msg):
    if msg.chat.type == "private":
        if msg.text == "☁️Weather":
            markup = types.InlineKeyboardMarkup(row_width = 4)
            weather_now = types.InlineKeyboardButton("Now", callback_data='wnow')
            weather_today = types.InlineKeyboardButton("Today", callback_data='wtoday')
            weather_tomorrow = types.InlineKeyboardButton("Tomorrow", callback_data='wtomorrow')
            weather_week = types.InlineKeyboardButton("Week", callback_data='wweek')
            markup.add(weather_now, weather_today, weather_tomorrow, weather_week)
            bot.send_message(msg.chat.id, "Choose the period", reply_markup=markup)
        elif msg.text == "🏠Change home city":
            pass
            

@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
    try:
        if call.message:
            if call.data == 'wnow':
                wnow = WeatherParser.get_weather_for_now("Moscow")
                temp = wnow.temperature("celsius")["temp"]
                temperature = "+" + str(temp) if temp >= 0 else "-" + str(temp)
                wind_speed = wnow.wind()["speed"]

                bot.send_message(call.message.chat.id, f"Now in <b>Moscow</b> <i>{wnow.detailed_status}</i> and temperature is <b>{temperature}</b> celsius. Speed of wind is <b>{wind_speed} m/s</b>, humidity is <b>{wnow.humidity}%</b>, clouds are <b>{wnow.clouds}</b>", parse_mode="html")
            elif call.data == "wtoday":
                pass
            elif call.data == "wtomorrow":
                pass
            elif call.data == "wweek":
                pass
    except Exception as e:
        print(repr(e))

bot.polling(none_stop = True)
        