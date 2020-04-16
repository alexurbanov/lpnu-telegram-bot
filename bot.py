import telebot
from telebot import types
import COVID19Py

covid19 = COVID19Py.COVID19()
bot = telebot.TeleBot('1081630485:AAEXd8y5xQ5jrLwE7SNgT6nl1uKx1kxy5vc')

# Функція, що спрацює при використанні команди Старт
# Тут ми створюємо швидкі кнопки, а також повідомлення з вітанням
@bot.message_handler(commands=['start'])
def start(message):
	markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
	btn1 = types.KeyboardButton('У всьому світі')
	btn2 = types.KeyboardButton('Україна')
	btn3 = types.KeyboardButton('США')
	btn4 = types.KeyboardButton('Китай')
	markup.add(btn1, btn2, btn3, btn4)

	send_message = f"<b>Привіт {message.from_user.first_name}!</b>\nЩоб дізнатися останню статистику розповсюдження коронавірусу напишіть: " \
		f"назву країни, наприклад: США, Украина, Білорусь, Китай, Японія і так далі\n"
	bot.send_message(message.chat.id, send_message, parse_mode='html', reply_markup=markup)

# Функція, що спрацює при відправці якого-небудь тексту боту
# Тут ми створюємо відстеження даних і висновок статистики по певній країні
@bot.message_handler(content_types=['text'])
def mess(message):
	final_message = ""
	get_message_bot = message.text.strip().lower()
	if get_message_bot == "сша":
		location = covid19.getLocationByCountryCode("US")
	elif get_message_bot == "україна":
		location = covid19.getLocationByCountryCode("UA")
	elif get_message_bot == "росія":
		location = covid19.getLocationByCountryCode("RU")
	elif get_message_bot == "білорусь":
		location = covid19.getLocationByCountryCode("BY")
	elif get_message_bot == "казахстан":
		location = covid19.getLocationByCountryCode("KZ")
	elif get_message_bot == "італія":
		location = covid19.getLocationByCountryCode("IT")
	elif get_message_bot == "франція":
		location = covid19.getLocationByCountryCode("FR")
	elif get_message_bot == "німеччина":
		location = covid19.getLocationByCountryCode("DE")
	elif get_message_bot == "японія":
		location = covid19.getLocationByCountryCode("JP")
	elif get_message_bot == "китай":
		location = covid19.getLocationByCountryCode("CN")
	else:
		location = covid19.getLatest()
		final_message = f"<u>Дані по всьому світі:</u>\n<b>Хворих: </b>{location['confirmed']:,}\n<b>Сметрей: </b>{location['deaths']:,}"

	if final_message == "":
		date = location[0]['last_updated'].split("T")
		time = date[1].split(".")
		final_message = f"<u>Дані по країні: <b>{get_message_bot.title()}</b></u>\nНаселення: {location[0]['country_population']:,}\n" \
				f"Останнє оновлення: {date[0]} {time[0]}\nОстанній дані:\n<b>" \
				f"Хворих: </b>{location[0]['latest']['confirmed']:,}\n<b>Сметрей: </b>" \
				f"{location[0]['latest']['deaths']:,}"

	bot.send_message(message.chat.id, final_message, parse_mode='html')

# Это нужно чтобы бот работал всё время
bot.polling(none_stop=True)