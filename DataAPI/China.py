import datetime
import os.path
import pandas as pd

from DataAPI.Base import OnlineDataSource, FileDataSource


class HongKong(OnlineDataSource):
    def __init__(self,initDate=datetime.date(2021, 12, 31)):
        super().__init__(
            'hongkong',
            '香港',
            7413100,
            uri='https://api.data.gov.hk/v2/filter?q=%7B%22resource%22%3A%22http%3A%2F%2Fwww.chp.gov.hk%2Ffiles%2Fmisc%2Flatest_situation_of_reported_cases_covid_19_chi.csv%22%2C%22section%22%3A1%2C%22format%22%3A%22json%22%2C%22filters%22%3A%5B%5B1%2C%22ct%22%2C%5B%22202%22%5D%5D%5D%7D',
            colsIn=['更新日期', '確診個案', '核酸檢測陽性的嚴重急性呼吸綜合症冠狀病毒2個案', '快速抗原測試陽性的嚴重急性呼吸綜合症冠狀病毒2個案'],
            colsMap={'更新日期':'date','確診個案':'pcr_pre22mar', '核酸檢測陽性的嚴重急性呼吸綜合症冠狀病毒2個案':'pcr_cases', '快速抗原測試陽性的嚴重急性呼吸綜合症冠狀病毒2個案':'latflow_cases'},
            initDate=initDate
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

class Beijing(FileDataSource):
    def __init__(self,initDate=datetime.date(2022, 4, 22)):
        super().__init__(
            'beijing',
            '北京', # 本土+境外输入
            24894300,
            initDate=initDate,
            uri=os.path.join('raw_data', 'beijing.csv')
        )

    def prepare(self):
        return super().prepare(minWindowSz=7)

    def connect(self):
        return pd.read_csv(self.uri, usecols=['date','acc_cases'])

    def df_postprocess(self, df):
        df['date'] = pd.to_datetime(df['date'], format='%Y/%m/%d').dt.date
        return df

class Shanghai(FileDataSource):
    def __init__(self,initDate=datetime.date(2022, 2, 26)):
        super().__init__(
            'shanghai',
            '上海', # 本土+境外输入
            25665000,
            initDate=initDate,
            uri=os.path.join('raw_data', 'shanghai.csv')
        )
    def connect(self):
        return pd.read_csv(self.uri, usecols=['date','acc_cases'])

    def df_postprocess(self, df):
        df['date'] = pd.to_datetime(df['date'], format='%Y/%m/%d').dt.date
        return df

class ShanghaiByDistrict(FileDataSource):
    def __init__(self):
        super().__init__(
            'shanghai_by_district',
            '上海',
            float('nan'),
            initDate=datetime.date(2022, 3, 27),
            uri=os.path.join('raw_data', 'shanghai_districts.csv')
        )
    def sync(self):
        print(f'Syncing data of {self.cityId} ...')
        print('', self.uri)
        df = self.connect()
        self.df = self.df_postprocess(df)
        self.state = 1
        print(f'Data of {self.cityId} synced.')
        return self.df

    def connect(self):
        _, fmt = self.uri.split('.')
        if fmt == 'xlsx':
            return pd.read_excel(self.uri)
        elif fmt == 'csv':
            return pd.read_csv(self.uri)

    def prepare(self, rounding=True):
        if self.state < 1:
            self.sync()
        
        print(f'Re-formatting data of {self.cityId} ...')
        print(f'Data of {self.cityId} re-formatted.')

        self.state = 2
        return self.df
    
    def df_postprocess(self, df, rounding=True):
        DIST_NAMES = (
            '浦东','黄浦','静安','徐汇','长宁','普陀','虹口','杨浦',
            '宝山','闵行','嘉定','金山','松江','青浦','奉贤','崇明',
        )
        df['日期'] = pd.to_datetime(df['日期'], format='%Y/%m/%d').dt.date
        for d in DIST_NAMES:
            df[d] = df[d].astype('int64')
            df[d + '_累计'] = df[d].cumsum()
            df[d + '_7日平均'] = df[d].rolling(window=7).mean()
        df = df.dropna()
        if rounding:
            for d in DIST_NAMES:
                df.loc[:,[d + '_7日平均']] = df.loc[:,[d + '_7日平均']].round(decimals = 0)
                df = df.astype({d + '_7日平均':'int64'})
        df = df[df['日期'] >= self.initDate]
        df.index.name = '天数'
        return df