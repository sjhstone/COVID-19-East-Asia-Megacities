import datetime
import os.path
import pandas as pd

from DataAPI.Base import OnlineDataSource, FileDataSource


class HongKong(OnlineDataSource):
    def __init__(self):
        super().__init__(
            'hongkong',
            '香港',
            uri='https://api.data.gov.hk/v2/filter?q=%7B%22resource%22%3A%22http%3A%2F%2Fwww.chp.gov.hk%2Ffiles%2Fmisc%2Flatest_situation_of_reported_cases_covid_19_chi.csv%22%2C%22section%22%3A1%2C%22format%22%3A%22json%22%2C%22filters%22%3A%5B%5B1%2C%22ct%22%2C%5B%22202%22%5D%5D%5D%7D',
            colsIn=['更新日期', '確診個案', '核酸檢測陽性的嚴重急性呼吸綜合症冠狀病毒2個案', '快速抗原測試陽性的嚴重急性呼吸綜合症冠狀病毒2個案'],
            colsMap={'更新日期':'date','確診個案':'pcr_pre22mar', '核酸檢測陽性的嚴重急性呼吸綜合症冠狀病毒2個案':'pcr_cases', '快速抗原測試陽性的嚴重急性呼吸綜合症冠狀病毒2個案':'latflow_cases'},
            initDate=datetime.date(2021, 12, 31)
        )
    
    def connect(self):
        return self.httpRequester(self.uri).json()
    
    def df_postprocess(self, df):
        df = df.rename(columns = self.colsMap)
        df['date'] = pd.to_datetime(df['date'], format='%d/%m/%Y').dt.date
        df.replace(r'^\s*$', 0, regex=True, inplace=True)
        df = df.astype({'pcr_pre22mar':'int64','pcr_cases':'int64','latflow_cases':'int64'})
        df['acc_cases'] = df['pcr_cases'] + df['latflow_cases'] + df['pcr_pre22mar']
        df.drop(columns=['pcr_cases', 'latflow_cases', 'pcr_pre22mar'], inplace=True)
        return df

class Shanghai(FileDataSource):
    def __init__(self):
        super().__init__(
            'shanghai',
            '上海',
            initDate=datetime.date(2022, 2, 26),
            uri=os.path.join('raw_data', 'shanghai.csv')
        )
    def connect(self):
        return pd.read_csv(self.uri, usecols=['date','acc_cases'])

    def df_postprocess(self, df):
        df['date'] = pd.to_datetime(df['date'], format='%Y/%m/%d').dt.date
        return df