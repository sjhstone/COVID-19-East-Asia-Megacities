import datetime
import requests
import pandas as pd

from DataAPI.Base import OnlineDataSource

class Seoul(OnlineDataSource):
    def __init__(self):
        super().__init__(
            'seoul',
            '서울',
            httpRequester=requests.post,
            uri='https://www.seoul.go.kr/coronaV/searchCoronaDayStatus.do',
            colsIn=['C_DATE2','HJ_ACC'], # 'GAP'
            colsMap={'C_DATE2':'date','HJ_ACC':'acc_cases',},
            initDate=datetime.date(2021, 12, 7)
        )
    
    def connect(self):
        return self.httpRequester(
            self.uri,
            data={
                'sdate': self.firstDay.strftime("%Y.%m.%d"),
                'edate': datetime.date.today().strftime("%Y.%m.%d")
            },
            headers={
                'Content-Type':'application/x-www-form-urlencoded'
            }
        ).json()['rVal']
    
    def df_postprocess(self, df):
        df = df.rename(columns = self.colsMap)
        df['date'] = pd.to_datetime(df['date'], format='%Y.%m.%d').dt.date
        df = df.astype({'acc_cases':'int64'})
        df.sort_values('date', inplace=True)
        return df
