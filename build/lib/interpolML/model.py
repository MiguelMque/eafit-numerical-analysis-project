import pandas as pd
from typing import Any


class Model:

    def __init__(self, name: str, model):
        self.name = name
        self.model = model

    def fit(self, train_dataset: pd.DataFrame):
        "Performs model training with standard settings"
        self.model.fit(train_dataset)

    def predict(self, dataset: Any):
        "Performs prediction"
        return self.model.predict(dataset)
