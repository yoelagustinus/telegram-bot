import requests as requests

url = "https://api.telegram.org/bot1453757504:AAENyCN0g_lqFfuaHL7gnJ84TPUZX95liHM/"

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

# main
def main():
	update_id = lastUpdate(url)["update_id"]
	while True:
		update = lastUpdate(url)
		if update_id == update["update_id"]:
			if getMessageText(update) == "hi" or getMessageText(update) == "halo":
				sendMessage(getChatId(update), "halo juga")
			else:
				sendMessage(getChatId(update), "Maaf, aku belum mengerti maksud kamu")
			update_id += 1

main()