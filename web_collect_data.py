from DataAPI import Korea, Japan, China
import datetime
# ordered by the date of the first local Omicron case

WEB_DATA_PATH = ''

cities = list()

cities.append(Korea.Seoul())
cities.append(Japan.Osaka())
cities.append(Japan.Tokyo())
cities.append(China.HongKong())
cities.append(China.Shanghai())
cities.append(China.Beijing())

for city in cities:
    city.save_webcsv(WEB_DATA_PATH)

China.ShanghaiByDistrict().save_webcsv(WEB_DATA_PATH)
