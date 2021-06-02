import pandas as pd
from keras.models import Sequential
from keras.layers import Dense, LSTM


class Model:

    def __init__(self, name: str, model):
        self.name = name
        self.model = model


    def fit(self, train_dataset : pd.DataFrame):
        "Performs model training with standard settings"

        self.model.fit()
