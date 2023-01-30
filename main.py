import telebot
import requests
import json

Api_Key = "5886161991:AAEgtfANerUZWylTLlvFtptPX2v3iNBHja0"
bot = telebot.TeleBot(Api_Key)
cid = ""
realData = ""
message_text = ""
user_name = ""
url = ""
data = ""
aslimaal = ""
freeKey = "EK-cgMkq-f79VYYW-u1JY5"
freeKey2 = "EK-pfZvx-FosL1Um-w77mG"
freeKey3 = "EK-22krG-VXcvgYY-jyyuo"
freeKey4 = "EK-6wZSf-zBCHfyy-ESj99"
freekey5 = "EK-af3uZ-LcuHf73-d1WJu"
freekey6 = "EK-8RsfJ-ckCnNW5-ddbmS"
sum = 0
specialAlpha = 0
gigaChad = 0
totalTxs = []


@bot.message_handler(commands=['start'])
def greet(message):
  bot.send_message(message.chat.id, "Paste The Contract Address")


def get_holders(array_of_objects, key):
  return [obj[key] for obj in array_of_objects]


def getContractHolders(url):
  #print(url)
  response_API = requests.get(url)
  #print(response_API.status_code)
  data = response_API.text
  realData = json.loads(data)
  #print(realData)
  maal = realData['holders']
  aslimaal = get_holders(maal, "address")
  #print(aslimaal)
  return aslimaal


def getTotalTxFromHolders(holders):
  for index, value in enumerate(holders):
    url = f"https://api.ethplorer.io/getAddressInfo/{value}?apiKey={freeKey}&showETHTotals=false"
    #print(url)
    response_API = requests.get(url)
    data = response_API.text
    trans = json.loads(data)
    totalTx = trans['countTxs']
    #print(totalTx)
    if 1 < totalTx < 10:
      global sum
      sum = sum + 1

    if 1 < totalTx < 6:
      global specialAlpha
      specialAlpha = specialAlpha + 1

    if 1 < totalTx < 4:
      global gigaChad
      gigaChad = gigaChad + 1

    if index == len(holders) - 1:
      print(sum, specialAlpha, gigaChad)


@bot.message_handler(func=lambda message: True)
def echo_message(message):
  message_text = message.text
  user_name = message.from_user.first_name
  bot.send_message(message.chat.id, f"Hey! {user_name} Searching Your Query")
  url = f"https://api.ethplorer.io/getTopTokenHolders/{message_text}?apiKey={freeKey}&limit=60"
  holders = getContractHolders(url)
  first_element = holders.pop(0)
  getTotalTxFromHolders(holders)
  bot.send_message(
    message.chat.id,
    f"There are {sum} fresh wallets {specialAlpha} Special Alpha and {gigaChad} GigaChad wallets"
  )


bot.polling()
