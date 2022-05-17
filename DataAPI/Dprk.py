import datetime
import os.path
import pandas as pd

from DataAPI.Base import OnlineDataSource, FileDataSource

class Pyongyang(FileDataSource):
    def __init__(self,initDate=datetime.date(2022, 5, 14)):
        super().__init__(
            'pyongyang',
            '평양',
            2870000,
            initDate=initDate,
            uri=os.path.join('raw_data', 'pyongyang.csv')
        )
    def connect(self):
        return pd.read_csv(self.uri, usecols=['date','acc_cases'])
    
    def prepare(self):
        return super().prepare(minWindowSz=1)

    def df_postprocess(self, df):
        df['date'] = pd.to_datetime(df['date'], format='%Y-%m-%d').dt.date
        return df
