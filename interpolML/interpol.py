import typing   

class interpolML:

    def __init__(self, initial_date : str, cut_date : str, end_date : str):

        self.initial_date = initial_date
        self.cut_Date = cut_date
        self.end_date = end_date
        self.data = self._generate_data()


    def _generate_data(self):
        from pandas_datareader.data import DataReader
        return DataReader('DOGE-USD', data_source='yahoo', start=self.initial_date, end=self.end_date).filter(["Close"])













#%%

