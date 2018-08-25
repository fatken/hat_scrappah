import time
import urllib.request, urllib.parse, urllib.error
from bs4 import BeautifulSoup
import json
import sys

from helper import *


def main(noPages, profileid, includeNA):
	#no of pages to scrap
	PAGES = int(noPages)#40
	#steam profile id
	PROFILEID = int(profileid)
	#whether to include NA in profit filter
	if includeNA.lower() == 'true':
		includeNA = True
	elif includeNA.lower() == 'false':
		includeNA = False
	else:
		print('invalid includeNA param!')
		return

	#1. inventory generation
	InventoryUrl = 'https://steamcommunity.com/inventory/' + str(PROFILEID)+ '/440/2?l=english&count=5000'

	response = urllib.request.urlopen(InventoryUrl)
	data = json.load(response)

	assets = data['assets']
	descriptions = data['descriptions']

	inventory = {}

	inventory = {}
	nameList = []
	not_tradable_count = 0
	for i in assets:
		classid = i['classid']
		for description in descriptions:
			if description['classid'] == classid:
				name = description['market_name']
				if description['tradable'] == 1:
					if name not in inventory:
						nameList.append(name)
						inventory[name] = {'classid': classid, 
											  'count': 1,
											  'tradable' : description['tradable']}
						break
					else:
						inventory[name]['count'] += 1
						break
	  
				else:
					not_tradable_count += 1
					break

	#2. scrap trade offers
	urlDefault = 'https://www.trade.tf/listings/'
	offerList = []
	pages = PAGES

	for pageNo in range(1, pages+1):
		print('scraping page',str(pageNo), '...', end = '\r')

		url = urlDefault + str(pageNo)
		headers = {'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:23.0) Gecko/20100101 Firefox/23.0'}  

		#html = urllib.request.urlopen(url, headers).read() #.read() reads the whole webpage instead of reading line by line
		req = urllib.request.Request(url=url, headers=headers)
		html = urllib.request.urlopen(req).read()
		soup = BeautifulSoup(html, 'html5lib')
		
		tradeDivs = soup.find_all('div', {'class': 'trade'})
		
		for trade in tradeDivs:
			tradeDict = tradeParse(trade)
			offerList.append(tradeDict)
		#time.sleep(5)
	print('scrapping complete')

	#3. filter trade offers
	profitableCount = 0
	for offer in offerList:
		green_flag = offerFilter(offer, inventory)
		if green_flag:
			profitable = profitFilter(offer['profit'],includeNA)
			if profitable:
				printOffer(offer)
				profitableCount += 1
	if profitableCount == 0:
		print('No profitable trades for now, try again later.')


if __name__ == '__main__':
	main(sys.argv[1], sys.argv[2], sys.argv[3])







