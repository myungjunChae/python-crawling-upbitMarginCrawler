#-*- coding: utf-8-*-
import time
import requests as rq
import os

from Queue import Queue
from bs4 import BeautifulSoup
from concurrent.futures import ProcessPoolExecutor
from concurrent.futures import ThreadPoolExecutor

SEED       = 3000000
BTC_price  = []

#coin_list  = ['SNT','ADA','BCC','XLM','POWR','XEM','NEO','LSK','LTC']
url = ""
coin_list  = ['ADA', 'SNT', 'NEO', 'ETH', 'XLM', 'XRP']

qTest = Queue()
coin_KRW_price = [] 
coin_BTC_price = [] 
sell_Direction = []

coin_margin = []
coin_count = len(coin_list)

def parsing():

	i = 0 #check 403 forbidden

	while i == 0:
		res = rq.get(url)
		li = res.text

		if li.find('Forbidden') == -1:
			i = 1;
		else:
			continue

		li = li.split(',')[6].split(':')[1]
		#PRICE_LIST.append(li.split(':')[1])

	return li

if __name__ == "__main__": 

	print('Start Crawling')

	#exe = ProcessPoolExecutor(max_workers = 4)

	loop = 0 
	with ThreadPoolExecutor(max_workers = 8) as exe:
		
		while loop == 0:

			start_time = time.time()

			del coin_KRW_price[:]
			del coin_BTC_price[:]
			del coin_margin[:]
			del BTC_price[:]
			del sell_Direction[:]
			qTest.queue.clear()
	      
			#parsing
			for i in range(coin_count):
				url = "https://crix-api-endpoint.upbit.com/v1/crix/candles/minutes/1?code=CRIX.UPBIT.KRW-" + coin_list[i] + "&count=1"
				temp = exe.submit(parsing)
				coin_KRW_price.append(temp.result())
				
				url = "https://crix-api-endpoint.upbit.com/v1/crix/candles/minutes/1?code=CRIX.UPBIT.BTC-" + coin_list[i] + "&count=1"
				temp = exe.submit(parsing)
				coin_BTC_price.append(temp.result())

			url = "https://crix-api-endpoint.upbit.com/v1/crix/candles/minutes/1?code=CRIX.UPBIT.KRW-" + 'BTC' + "&count=1"
			temp = exe.submit(parsing)
			BTC_price.append(temp.result())

			#BTC price -> KRW price
			for i in range(coin_count):
				temp = (float)(coin_BTC_price[i])
				temp *= (float)(BTC_price[0])
				coin_BTC_price[i] = (str)(temp)

			#Remove Decimals
			for i in range(coin_count):
				coin_KRW_price[i] = coin_KRW_price[i].split('.')[0]
				coin_BTC_price[i] = coin_BTC_price[i].split('.')[0]

			#Calculate Margin
			for i in range(coin_count):
				BTC = (int)(coin_BTC_price[i])
				KRW = (int)(coin_KRW_price[i])


				if BTC > KRW :
					percentage = ((float)(BTC- KRW)/KRW) * 100 - 0.35
					sell_Direction.append("KRW -> BTC")
				else :
					percentage = ((float)(KRW- BTC)/BTC) * 100 - 0.35
					sell_Direction.append("BTC -> KRW")

				realBenefit = (SEED * percentage) / 100

				#print(percentage)
				#print(realBenefit)

				coin_margin.append(percentage)

			#Remove Prevent Data
			os.system('cls')

			#Print Result
			for i in range(coin_count):

				if coin_margin[i] > 0.2:

					#if coin_margin[i] > 0 :
					print('{:5}'.format((str)(coin_list[i]))),
					print(' : '),
					print('{:5.2f}'.format((float)(coin_margin[i]))),
					print('        '),
					print('{:7}'.format(coin_KRW_price[i])),
					print(' |  '),
					print('{:10}'.format(coin_BTC_price[i])),
					print(sell_Direction[i])

			#loop = 1      

			print("-- %s seconds ---" % (time.time() - start_time))   
         
