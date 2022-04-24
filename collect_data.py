from DataAPI import Korea, Japan, China
# ordered by the date of the first local Omicron case

cities = [Korea.Seoul(), Japan.Osaka(), Japan.Tokyo(), China.HongKong(), China.Shanghai()]

for city in cities:
    city.save_csv('data')
    city.save_pickle('data')
