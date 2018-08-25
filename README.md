# hat_scrappah
This scrappah find good trading offers from a TF2 trading site so I can find all the good deals and trade and get filthy rich and stuff.LUL


The crawler first extracts the users TF2 inventory based on his or her steam ID, then from a TF2 trading site, it finds all the profitable offers that are trading for items the user have in his inventory and return offer information to the user.

The crawler is missing steam login functionality, which is required to extract some offer URLs. For now it shows some URLs if available and also extracts URL in offer description. I will try to add steam login functionality later.

TF2交易爬虫

这个爬虫首先根据steamID获取用户的TF2背包物品信息，之后爬取一个TF2交易平台上的交易信息，并找出所有该用户可以进行（用户有交易交换的物品）且有利可图的交易，并返回交易信息。

本爬虫缺少steam login功能，所以不能获取有些交易的URL.以后我会尝试加入steam login功能。

`python3 hat_scrappah.py [NO_OF_PAGES_TO_SCRAP] [STEAM_ID]`
