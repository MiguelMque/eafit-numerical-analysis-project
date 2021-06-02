
from typing import Any
import pandas as pd

class Model:

    def __init__(self, name: str, model, freq:str):
        self.name = name
        self.model = model
        self.freq = freq
        self.train = None

    def fit(self, train_dataset):

        "Performs model training with standard settings"
        self.train = train_dataset

        if self.name == "orbit":

            self.model.fit(train_dataset)

        elif self.name == "nprophet":
            self.model.fit(train_dataset, validate_each_epoch=True,
                    valid_p=0.2, freq=self.freq,
                    plot_live_loss=True, epochs=10)

    def predict(self, dataset: Any):
        "Performs prediction"

        if self.name == "orbit":
            prediction = self.model.predict(dataset)
        elif self.name == "nprophet":

            future = self.model.make_future_dataframe(self.train, periods=len(dataset))
            prediction = self.model.predict(future)

        return prediction