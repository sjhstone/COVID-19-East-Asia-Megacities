import datetime
import requests
import pandas as pd
import os.path

class DataSource:
    def __init__(self, cityId, cityName, population, initDate, target='py'):
        self.state = 0
        self.cityId = cityId
        self.cityName = cityName
        self.initDate = initDate
        self.population = population
        self.df = None
        self.firstDay = self.initDate - datetime.timedelta(days=7)
        self.target = target

    def prepare(self, rounding=True, tAvgWindow=7, minWindowSz=7):
        if self.state < 1:
            self.sync()
        
        print(f'Re-formatting data of {self.cityId} ...')
        self.df = self.df[self.df['date'] >= self.firstDay]
        
        self.df['daily_cases'] = self.df['acc_cases'].diff()
        self.df = self.df.dropna()
        
        self.df = self.df.astype({'acc_cases':'int64','daily_cases':'int64'})
        
        self.df['cases_7dma'] = self.df['daily_cases'].rolling(window=tAvgWindow, min_periods=minWindowSz).mean()
        self.df = self.df.dropna()
        if rounding:
            self.df['cases_7dma'] = self.df['cases_7dma'].round(decimals = 0)
            self.df = self.df.astype({'cases_7dma':'int64'})

        self.df['acc_cases'] = self.df['daily_cases'].cumsum()
        self.df = self.df.reset_index(drop=True)

        if self.target == 'web':
            self.df['累计占总人口'] = self.df['acc_cases'] * 100 / self.population
            self.df['累计占总人口'] = self.df['累计占总人口'].map('{:,.2f}%'.format)
            self.df.index.name = '天数'
            self.df = self.df.rename(columns = {
                'date': '日期',
                'acc_cases': '累计',
                'daily_cases': '日增',
                'cases_7dma': '近7日平均日增',
            })
        
        self.state = 2
        print(f'Data of {self.cityId} re-formatted.')
        return self.df
    
    def save_pickle(self, path):
        if self.state < 2:
            self.prepare()
        self.df.to_pickle(os.path.join(path, f'{self.cityId}.pkl'))
        print(f'Data of {self.cityId} saved as pickle.')
        return 1
        
    def save_csv(self, path):
        if self.state < 2:
            self.prepare()
        self.df.to_csv(os.path.join(path, f'{self.cityId}.csv'))
        print(f'Data of {self.cityId} saved as csv.')
        return 1
    
    def save_webcsv(self, path):
        if self.state < 2:
            self.target = 'web'
            self.prepare(rounding=True)
        self.df.to_csv(os.path.join(path, f'{self.cityId}.csv'))
        print(f'Data of {self.cityId} saved as csv for web.')
        return 1


class OnlineDataSource(DataSource):
    def __init__(
        self, cityId, cityName, population,
        httpRequester=requests.get,
        uri=None,
        colsIn=list(),
        colsMap=dict(),
        initDate=datetime.date(2021, 12, 7)
    ):
        super().__init__(cityId, cityName, population, initDate)
        self.httpRequester = httpRequester
        self.uri = uri
        self.colsIn = colsIn
        self.colsMap = colsMap
    
    def sync(self):
        print(f'Syncing data of {self.cityId} ...')
        print('', self.uri)
        self.df = pd.DataFrame(self.connect(), columns=self.colsIn)
        self.df = self.df_postprocess(self.df)
        self.state = 1
        print(f'Data of {self.cityId} synced.')
        return self.df

class FileDataSource(DataSource):
    def __init__(
        self, cityId, cityName, population, initDate, uri
    ):
        super().__init__(cityId, cityName, population, initDate)
        self.uri = uri
    
    def sync(self):
        print(f'Syncing data of {self.cityId} ...')
        print('', self.uri)
        self.df = self.connect()
        self.df = self.df_postprocess(self.df)
        self.state = 1
        print(f'Data of {self.cityId} synced.')
        return self.df
