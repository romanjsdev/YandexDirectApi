import requests
import json


token = ''

clientLogin = ''

adsURL = 'https://api-sandbox.direct.yandex.com/json/v5/ads'
campURL = 'https://api-sandbox.direct.yandex.com/json/v5/campaigns'
headers = {"Authorization": "Bearer " + token,
           "Client-Login": clientLogin, 
           "Accept-Language": "ru",  
           }

getCapm = {"method": "get",
        "params": {"SelectionCriteria": {},
                   "FieldNames": ["Id", "Name"] 
                   }} 

getCapm = json.dumps(getCapm)

#Получаем Id всех компаний 
campaigns = []
res = requests.post(campURL, getCapm, headers=headers)
for camp in res.json()["result"]["Campaigns"]:
	campaigns.append(camp["Id"])

#Получаем все активные объявления во всех компаниях
getAds = {"method": "get",
        "params": {"SelectionCriteria": {
        	"CampaignIds": campaigns,
        	"States":["ON"]
        	}, 
                   "FieldNames": ["CampaignId", "Id", "State", "Status"],
                   "TextAdFieldNames":["Title", "Title2" ]
            }}
getAds = json.dumps(getAds)
result = requests.post(adsURL, getAds, headers=headers)

#Создаем массив с Id всех актиных объявлений
adsId = []
if result.json()["result"]!={}:
	for res in result.json()["result"]["Ads"]:
		print(res)
		adsId.append(res["Id"])
else:
	print("Error: Обьявления не найдены")

#Новый второй заголовок
title2 = "Lorem ipsum"

#Изменяем второй заголовок в оъявлениях
for adID in adsId:
	updateAds = {
  					"method": "update",
  					"params": { 
    							"Ads": [{
      								"Id": adID,
      								"TextAd": {
        								"Title2": title2 
        								}
        							}]
        						}
        		}

	updateAds = json.dumps(updateAds)
	result = requests.post(adsURL, updateAds, headers=headers)
	print(result.json())