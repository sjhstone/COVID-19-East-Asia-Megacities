import datetime
import requests
import pandas as pd
import os.path

class DataSource:
    def __init__(self, cityId, cityName, initDate):
        self.state = 0
        self.cityId = cityId
        self.cityName = cityName
        self.initDate = initDate
        self.df = None
        self.firstDay = self.initDate - datetime.timedelta(days=7)

    def prepare(self):
        if self.state < 1:
            self.sync()
        
        print(f'Re-formatting data of {self.cityId} ...')
        self.df = self.df[self.df['date'] >= self.firstDay]
        
        self.df['daily_cases'] = self.df['acc_cases'].diff()
        self.df = self.df.dropna()
        
        self.df = self.df.astype({'acc_cases':'int64','daily_cases':'int64'})
        
        self.df['cases_7dma'] = self.df['daily_cases'].rolling(window=7).mean()
        self.df = self.df.dropna()

        self.df['acc_cases'] = self.df['daily_cases'].cumsum()
        self.df = self.df.reset_index(drop=True)
        
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


class OnlineDataSource(DataSource):
    def __init__(
        self, cityId, cityName,
        httpRequester=requests.get,
        uri=None,
        colsIn=list(),
        colsMap=dict(),
        initDate=datetime.date(2021, 12, 7)
    ):
        super().__init__(cityId, cityName, initDate)
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
        self, cityId, cityName, initDate, uri
    ):
        super().__init__(cityId, cityName, initDate)
        self.uri = uri
    
    def sync(self):
        print(f'Syncing data of {self.cityId} ...')
        print('', self.uri)
        self.df = self.connect()
        self.df = self.df_postprocess(self.df)
        self.state = 1
        print(f'Data of {self.cityId} synced.')
        return self.df
    
    def prepare(self):
        if self.state < 1:
            self.sync()
        
        print(f'Re-formatting data of {self.cityId} ...')
        self.df = self.df[self.df['date'] >= self.firstDay]
        
        self.df['daily_cases'] = self.df['acc_cases'].diff()
        self.df = self.df.dropna()
        
        self.df = self.df.astype({'acc_cases':'int64','daily_cases':'int64'})
        
        self.df['cases_7dma'] = self.df['daily_cases'].rolling(window=7).mean()
        self.df = self.df.dropna()

        self.df['acc_cases'] = self.df['daily_cases'].cumsum()
        self.df = self.df.reset_index(drop=True)
        
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