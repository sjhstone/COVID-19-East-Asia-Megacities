import datetime
import os.path
import pandas as pd

from DataAPI.Base import OnlineDataSource, FileDataSource

class Dprk(FileDataSource):
    def __init__(self,initDate=datetime.date(2022, 4, 29)): # 仅5月13日起数据为官方披露
        super().__init__(
            'DPRK',
            'DPRK',
            initDate=initDate,
            uri=os.path.join('raw_data', 'dprk.csv')
        )
    def connect(self):
        return pd.read_csv(self.uri, usecols=['date','acc_cases'])

    def df_postprocess(self, df):
        df['date'] = pd.to_datetime(df['date'], format='%Y-%m-%d').dt.date
        return df
