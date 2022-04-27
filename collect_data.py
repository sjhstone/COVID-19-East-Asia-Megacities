from DataAPI import Korea, Japan, China
# ordered by the date of the first local Omicron case

cities = list()
cities.append(Korea.Seoul())
cities.append(Japan.Osaka())
cities.append(Japan.Tokyo())
cities.append(China.HongKong())
cities.append(China.Shanghai())
cities.append(China.ShanghaiByDistrict())

for city in cities:
    city.save_csv('data')
    city.save_pickle('data')
