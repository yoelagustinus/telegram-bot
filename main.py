import telebot

bot = telebot.TeleBot('1453757504:AAENyCN0g_lqFfuaHL7gnJ84TPUZX95liHM')

@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message, 'Hello')


print('bot is running')
bot.polling()