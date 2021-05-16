import pandas as pd
from keras.models import Sequential
from keras.layers import Dense, LSTM


class Model:
    import numpy as np
    def __init__(self, data : pd.DataFrame):
        self.data = data
        

