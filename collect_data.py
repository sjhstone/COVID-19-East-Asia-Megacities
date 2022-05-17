from DataAPI import Korea, Japan, China, Dprk
import datetime
# ordered by the date of the first reported local community-spreaded Omicron case,
# or first day with reported case number > 10 in the most current wave

webfile_base = '..\\COVID_JS_INTERACTIVE\\covid_5cities_jsdist\\covid\\'

cities = list()

cities.append(Korea.Seoul()) # cities.append(Korea.Seoul(initDate=datetime.date(2021,10,23)))

cities.append(Japan.Osaka())
cities.append(Japan.Tokyo())

cities.append(China.HongKong())
cities.append(China.Shanghai())
cities.append(China.Beijing())
cities.append(China.GreaterTaipei())

cities.append(Dprk.Pyongyang())


for c in cities:
    try:
        c.save_csv('data')
        c.save_pickle('data')
        c.save_webcsv(webfile_base + 'data')
    except:
        print(c.cityId, 'skipped')
        continue

China.ShanghaiByDistrict().save_csv(webfile_base + 'districts')
