import datetime
import pandas as pd

from DataAPI.Base import OnlineDataSource

class Japan(OnlineDataSource):
    def __init__(self, cityId, cityName, initDate):
        super().__init__(
            cityId,
            cityName,
            uri=f'https://opendata.corona.go.jp/api/Covid19JapanAll?dataName={cityName}',
            colsIn=['date','npatients'],
            colsMap={'npatients':'acc_cases',},
            initDate=initDate
        )
    
    def connect(self):
        return self.httpRequester(self.uri).json()['itemList']
    
    def df_postprocess(self, df):
        df = df.rename(columns = self.colsMap)
        df['date'] = pd.to_datetime(df['date'], format='%Y-%m-%d').dt.date
        df = df.astype({'acc_cases':'int64'})
        df.sort_values('date', inplace=True)
        return df


class Tokyo(Japan):
    def __init__(self):
        super().__init__('tokyo', '東京都', datetime.date(2021, 12, 24))

class Osaka(Japan):
    def __init__(self):
        super().__init__('osaka', '大阪府', datetime.date(2021, 12, 22))