import requests as requests
import random
import string
import re

# import word_tokenize from nltk module
from nltk.tokenize import word_tokenize

# import class UserBotInteraction 
from model import UserBotInteraction

# import class StemmingText
from controller import StemmingText 

# TOKEN API
url = "https://api.telegram.org/bot1475966158:AAG55_LakcRnde2olpyGn2PaxV-wH051zG0/"

# get chat id
def getChatId(update):
	chat_id = update["message"]["chat"]["id"]
	return chat_id

# get message text
def getMessageText(update):
	message_text = update["message"]["text"]
	message_text.lower()
	return message_text

# get last record messsage update
def lastUpdate(req):
	response = requests.get(req + "getUpdates")
	response = response.json()
	result = response["result"]
	total_updates = len(result) - 1
	return result[total_updates]

# send message
def sendMessage(chat_id, message_text):
	params = {"chat_id": chat_id, "text": message_text}
	response = requests.post(url + "sendMessage", data=params)
	return response

# reply message
def replyMessage(text, harga_twr, jml_baju, baju1, baju2):
	# proses
	text = StemmingText.stemmingText(text)
	# proses tokenize
	tokens = word_tokenize(text)

	reply = ""
	list_word = []

	for word in tokens:
		list_word.append(word)	# menyimpan word ke dalam list

		# reply greeting
		if word in UserBotInteraction.USER_GREETINGS:
			reply += random.choice(UserBotInteraction.BOT_GREETINGS) + ". "
		if any(w in list_word for w in UserBotInteraction.USER_HOW_ARE_YOU_1) and any(w in list_word for w in UserBotInteraction.USER_HOW_ARE_YOU_2):
			reply += random.choice(UserBotInteraction.BOT_HOW_ARE_YOU)

		#basa-basi
		if any(w in list_word for w in UserBotInteraction.USER_BASA_BASI_1):
			reply += random.choice(UserBotInteraction.BOT_BASA_BASI_1)
		# reply thank you
		if word in UserBotInteraction.USER_THANK_YOU:
			reply += random.choice(UserBotInteraction.BOT_YOU_ARE_WELCOME)

	# reply beli baju
	if any(w in tokens for w in ['type01']) and any(w in tokens for w in ['nego']):
		if harga_twr[0] < baju1[2]:
			reply += "owh maap kak, tidak bisa"
		else:
			reply += "bisa ka! fix ga?"
	elif any(w in tokens for w in ['type02']) and any(w in tokens for w in ['nego']):
		if harga_twr[0] < baju2[2]:
			reply += "owh maap kak, tidak bisa"
		else:
			reply += "bisa ka! fix ga?"
	elif any(w in tokens for w in ['type01']) and any(w in tokens for w in ['final']) and any(w in tokens for w in ['order']):
		if harga_twr[0] >= baju1[2]:
			reply+= "type01, totalnya jadi " + str(harga_twr[0]*jml_baju[1])
		else:
			reply+="wah harga tawarnya salah tuh kak"
	elif any(w in tokens for w in ['type02']) and any(w in tokens for w in ['final']) and any(w in tokens for w in ['order']):
		if harga_twr[0] >= baju2[2]:
			reply+= "type02, totalnya jadi " + str(harga_twr[0]*jml_baju[1])
		else:
			reply+="wah harga tawarnya salah tuh kak"
	elif any(w in tokens for w in ['type01']) and any(w in tokens for w in ['jumlah']):
		reply += "totalnya jadi " + str(jml_baju[0] * baju1[1])
		baju1[2] *= jml_baju[0]
	elif any(w in tokens for w in ['type02']) and any(w in tokens for w in ['jumlah']):
		reply += "totalnya jadi " + str(jml_baju[0] * baju2[1])
		baju2[2] *= jml_baju[0]
	elif any(w in tokens for w in ['beli']) and any(w in tokens for w in ['baju']) and any(w in tokens for w in ['type01']) or any(w in tokens for w in ['type01']):
		reply += "mau beli berapa?\n\nKetik '*nama baju* jumlah *jumlah yang diinginkan*'"
	elif any(w in tokens for w in ['beli']) and any(w in tokens for w in ['baju']) and any(w in tokens for w in ['type02']) or any(w in tokens for w in ['type02']):
		reply += "mau beli berapa?\n\nKetik '*nama baju* jumlah *jumlah yang diinginkan*'"
	elif any(w in tokens for w in ['beli']) and any(w in tokens for w in ['baju']) or any(w in tokens for w in ['beli']):
		reply += (
			"mau beli baju apa? ini baju-baju yang toko kami jual.\n" 
			"1. Type01 = 120000\n"
			"2. Type02 = 150000\n\n"
			"Ketik '*nama baju*' untuk memilih baju"
		)
	elif any(w in tokens for w in ['tawar']) or any(w in tokens for w in ['kurang']):
		reply += (
			"boleh, maunya berapa?\n\n"
			"Ketik 'nego *nama baju* *harga yang diinginkan*"
		)
	elif any(w in tokens for w in ['fix']) or any(w in tokens for w in ['oke']):
		reply += "Ketik 'final order *baju* *harga yang sepakat* *jumlah*' untuk membeli"

	return reply

# main
def main():
	MIN_HARGA_TAWAR_BAJU_1 = 100000
	MIN_HARGA_TAWAR_BAJU_2 = 135000

	update_id = lastUpdate(url)["update_id"]

	while True:
		# data produk baju
		data_baju_1 = ['type01', 120000, MIN_HARGA_TAWAR_BAJU_1]
		data_baju_2 = ['type02', 150000, MIN_HARGA_TAWAR_BAJU_2]

		update = lastUpdate(url)
		user_reply=getMessageText(update)

		harga_tawar = [int(s) for s in str.split(user_reply) if s.isdigit()]
		jumlah_baju = [int(s) for s in str.split(user_reply) if s.isdigit()]

		if update_id == update["update_id"]:
			if user_reply == "/start":
				sendMessage(getChatId(update), "Selamat datang Dinego, silahkan beli baju yang anda inginkan. Kalau harga tidak cocok, boleh dinego kok!\n\nKetik 'beli' atau 'beli baju' untuk mulai membeli")
			elif user_reply == "/help":
				sendMessage(getChatId(update), "")           
			else:
				bot_respon = replyMessage(user_reply, harga_tawar, jumlah_baju, data_baju_1, data_baju_2)
				sendMessage(getChatId(update), bot_respon)

			update_id += 1

main()