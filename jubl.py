import bs4 as bs
import urllib.request
from urllib.request import urlopen
from bs4 import BeautifulSoup
import pandas as pd
import re

def moneycontrol():
	mony_page = "https://www.moneycontrol.com/india/fnoquote/jubilantfood/JF04/2019-01-31"
	mony_open = urlopen(mony_page)
	
	soup = bs.BeautifulSoup(mony_open,'lxml')
	type(soup)
	
	#mony_price = soup.find_all('p')
	mony_Oprice = soup.find_all('tr')
	
	print (mony_Oprice[1:2])
	#print (mony_price[13:14]) - Current PRice Location
	#print (mony_price[14:15]) - % Price Change
	
#	for m in mony_price[13:14]:
#		strong=m.find_all('strong')
#		m_row= [i.text for i in strong]
#		df0 = pd.DataFrame(m_row)
#		Cur_Price = float(df0.iloc[0])
#	print ("Current Price: ", Cur_Price)
	
#	for m in mony_price[14:15]:
#		strong=m.find_all('strong')
#		m_row= [i.text for i in strong]
#		df0 = pd.DataFrame(m_row)
#		Price_chng = float(df0.iloc[0])
#	print ("Price Change: ", Price_chng)
	  
#	for m in mony_)price[:15]:
#		td =m.find_all('td')
#		m_row= [i.text for i in td]
#		print (m_row)
#		df0 = pd.DataFrame(m_row)
#		O_Price = float(df0.iloc[0])

#	print ("Open Price : ", O_Price)
	
	
def Topstockresearch():
	
	## *************************************** EXTRACTING CURRENT FUTURE PRICE FROM MONEY CONTROL *****************************************
	mony_page = "https://www.moneycontrol.com/india/fnoquote/jubilantfood/JF04/2019-01-31"
	mony_open = urlopen(mony_page)
	
	soup = bs.BeautifulSoup(mony_open,'lxml')
	type(soup)
	
	mony_price = soup.find_all('p')

	## ************************************** EXTRACTING Current PRICE ******************************************************************
	for m in mony_price[13:14]:
		strong=m.find_all('strong')
		m_row= [i.text for i in strong]
		df0 = pd.DataFrame(m_row)
		Cur_Price = float(df0.iloc[0])
	
	## ************************************** EXTRACTING OPEN PRICE ******************************************************************
	mony_Oprice = soup.find_all('tr')
	for m in mony_Oprice[1:2]:
		td=m.find_all('td')
		m_row1= [i.text for i in td]
		df0 = pd.DataFrame(m_row1)
		df1 = df0[0].str.split(',', expand=True)
		O_Price = df1.iloc[0]
	
	## *************************************** EXTRACTING PIVOT POINTS FROM TOPSTOCKRESEARCH *****************************************
	
	jub_page = "https://www.topstockresearch.com/INDIAN_STOCKS/FOOD_AND_FOOD_PROCESSING/FuturesAndOptionAnalysisOfJubliant_Foodworks_Limited.html"
	jub_open = urlopen(jub_page)
	
	Fut_Price = Cur_Price

	soup = bs.BeautifulSoup(jub_open,'lxml')
	type(soup)
	#bs4.BeautifulSoup
	#title = soup.get_text()
	title = soup.find_all('tr')
	#print (title[13:15])


	for t in title[13:15]:
		td=t.find_all('td')
		th = t.find_all('th')
		row = [i.text for i in td]
	
		df0=pd.DataFrame(row)
	#	print(header)
	
	df1 = df0[0].str.split(',', expand=True)

	#print(df1.head(10))

	#Expiry_date= date(df1.loc[0])
	#Cur_Price = float(df1.loc[1]) 
	#Fut_Price = float(df1.loc[2]) - Will Take Fut Price from Money Control
	Piv_point = float(df1.loc[3])
	Support1 = float(df1.loc[4])
	Support2 = float(df1.loc[5])
	Support3 = float(df1.loc[6])
	Resistance1 = float(df1.loc[7])
	Resistance2 = float(df1.loc[8])
	Resistance3 = float(df1.loc[9])

	print("Current Future Price: ",Fut_Price)
	#print("Open Future Price: ",O_Price)
	
	
	if Fut_Price > Piv_point and Fut_Price < Resistance1:
		print("Alert for Jubliant Short @", Resistance1)
	elif Fut_Price < Piv_point and Fut_Price > Support1:
		print("Alert for Jubliant Long @", Support1)
		text = "Alert for Jubliant Long @" + str(Support1)
		#url =  Url + "sendMessage?text={}&chat_id={}".format(text, chat_id)
	elif Fut_Price > Support2 and Fut_Price < Support1:
		print("Alert for Jubliant Long @", Support2)
	elif Fut_Price > Support3 and Fut_Price < Support2:
		print("Alert for Jubliant Long@", Support3)
	elif Fut_Price > Resistance1 and Fut_Price < Resistance2:
		print("Alert for Jubliant Short @", Resistance2)
	elif Fut_Price > Resistance2 and Fut_Price < Resistance3:
		print("Alert for Jubliant Short @", Resistance3)
	
	return text
	
import json 
import requests
import time

TOKEN = "673584086:AAEIlo-adMnnVFTe8YF_QTO2QJal3MS8JfA"			
URL = "https://api.telegram.org/bot{}/".format(TOKEN)
chat_id ="603693857"


def get_url(url):
    response = requests.get(url)
    content = response.content.decode("utf8")
    return content


def get_json_from_url(url):
    content = get_url(url)
    js = json.loads(content)
    return js


def get_updates(offset=None):
    url = URL + "getUpdates?timeout=100"
    if offset:
        url += "&offset={}".format(offset)
    js = get_json_from_url(url)
    return js

def get_last_chat_id_and_text(updates):
    num_updates = len(updates["result"])
    last_update = num_updates - 1
    text = updates["result"][last_update]["message"]["text"]
    chat_id = updates["result"][last_update]["message"]["chat"]["id"]
    return (text, chat_id)

def get_last_update_id(updates):
    update_ids = []
    for update in updates["result"]:
        update_ids.append(int(update["update_id"]))
    return max(update_ids)


def echo_all(updates):
    for update in updates["result"]:
        try:
            text = Topstockresearch()
			#text = update["message"]["text"]
            chat = update["message"]["chat"]["id"]
            send_message(text, chat)
        except Exception as e:
            print(e)
			
def send_message(text, chat_id):
    text = urllib.parse.quote_plus(text)
    url = URL + "sendMessage?text={}&chat_id={}".format(text, chat_id)
    get_url(url)
	    
#text, chat = get_last_chat_id_and_text(get_updates())
#send_message(text, chat)
	
def main():
    last_update_id = None
    while True:
        updates = get_updates(last_update_id)
        if len(updates["result"]) > 0:
            last_update_id = get_last_update_id(updates) + 1
            echo_all(updates)
        time.sleep(0.5)
			
if __name__ == "__main__":
	main()
	#Cur_Price = 0
	#moneycontrol()
	Topstockresearch()
	