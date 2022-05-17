from DataAPI import Korea, Japan, China, Dprk
import datetime
# ordered by the date of the first reported local community-spreaded Omicron case

cities = list()
cities.append(Korea.Seoul()) # cities.append(Korea.Seoul(initDate=datetime.date(2021,10,23)))
cities.append(Japan.Osaka())
cities.append(Japan.Tokyo())
cities.append(China.HongKong())
cities.append(China.Shanghai())
cities.append(China.Beijing())
cities.append(Dprk.Pyongyang())

for c in cities:
    try:
        c.save_csv('data')
        c.save_pickle('data')
        c.save_webcsv('..\\COVID_JS_INTERACTIVE\\covid_5cities_jsdist\\covid\\data')
    except:
        print(c.cityId, 'skipped')
        continue

China.ShanghaiByDistrict().save_webcsv('..\\COVID_JS_INTERACTIVE\\covid_5cities_jsdist\\covid\\districts')
