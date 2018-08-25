import re
import numpy as np



#1. inventory generation
def itemExtactor(item):
    itemName = item.find('div', {'class':'trade-item-title'}).text.strip()
    itemCount = item.find('span', {'class':'label label-inverse'})
    if itemCount:
        itemCount = itemCount.text
        strPtn = re.compile('x(.*)')
        itemCount = float(re.findall(strPtn, itemCount)[0])
    else:
        itemCount = 1
    return itemName, itemCount


#2. trade offer parser
def tradeParse(trade):
    '''
    tradeParse() takes in trade HTML soup as input,
    parses it and return a trade offer dict.
    '''

    tradeDict = {}
    #user name
    userName = trade.find('span', {'class':'trade-header-title-name-user'}).text.strip()
    if userName == '[unknown user]':
        userName = 'unknown user'

    #description
    description = trade.find('div', {'class': 'trade-header-notes'}).text.strip().replace('\n', ' ')
    ptn = re.compile('(http\S*)')
    descriptionUrl = re.findall(ptn, description)

    #url
    url = trade.a.get('href')
    if url == '#modal_signin':
        url = 'sign in needed'
    else: url = 'https://www.trade.tf' + url

    #profit
    profit = trade.find('span', {'class':'trade-profit'}).text.strip()
    if profit == 'n/a':
        profit = np.NAN
    else:
        profit = float(profit.rstrip('%'))

    #trade detail
    classNames = re.compile('trade-block[1-3]')
    parts = trade.find_all('div', {'class': classNames})#find_all('div', {'class':'trade-item-title'}))

    sellingDict = {}
    buyingDict = {}

    sellingItems = parts[0].find_all('div', {'class':'trade-item'})    
    for item in sellingItems:
        itemName, itemCount = itemExtactor(item)
        sellingDict[itemName] = itemCount

    buyingItems = parts[1].find_all('div', {'class':'trade-item'})
    for item in buyingItems:
        itemName, itemCount = itemExtactor(item)
        buyingDict[itemName] = itemCount

    tradeDict = {
    'userName': userName,
    'description':description,
    'url':url,
    'profit':profit,
    'selling': sellingDict, 
    'buying': buyingDict    
    }

    if descriptionUrl:
        tradeDict['descriptionUrl'] = descriptionUrl
    return tradeDict

# 3. trade offer filter function
def offerFilter(offer, inventory):
    '''
    filter out offers buying items not included in the inventory of the user.
    takes in offer, return whether the offer is "doable"
    '''
    green_flag = 1
    buyingItemsDict = offer['buying']
    for item in buyingItemsDict:
        #print(item)
        if item not in inventory or buyingItemsDict[item] > inventory[item]['count']:
            green_flag = 0
            return green_flag
    return green_flag

#4. profit filter function
def profitFilter(profit, includeNA=True):
    '''
    takes in profit and condition whether or not to include NA as profitable, include NA by default
    return 1 if profitable
    return 0 if not profitable
    '''
    if (includeNA and np.isnan(profit)) or profit > 0:
        return 1
    else:
        return 0
def printOffer(offer):
    print('profitable')
    print('name:', offer['userName'])
    print('description:', offer['description'])
    print('URL:', offer['url'])
    #if contain URL in description:
    if offer.get('descriptionUrl'):
        print('description url:')
        for descriptionUrl in offer['descriptionUrl']:
            print(descriptionUrl)
    print('SELLING:')
    for i in offer['selling'].keys():
        print(i, 'X', offer['selling'][i])
    print('BUYING:')
    for i in offer['buying'].keys():
        print(i, 'X', offer['buying'][i])
    print('profit:', offer['profit'])
    print('-'*20, '\n')



