from orbit.diagnostics.plot import plot_predicted_data
from interpolML.model import Model
import numpy as np


class Plotter:

    def __init__(self, model: Model):
        self.train = model.train
        self.predicted = model.prediction
        self.test = model.test
        self.date_col = model.date_col
        self.y_col = model.y_col

    def plot_predicted_data(self):
        ci = 2.576 * np.std(self.predicted.prediction) / np.mean(self.predicted.prediction)
        self.predicted["prediction_5"] = self.predicted.prediction - ci
        self.predicted["prediction_95"] = self.predicted.prediction + ci

        print(self.predicted)

        plot_predicted_data(self.train, self.predicted, self.date_col, self.y_col, test_actual_df=self.test,
                            prediction_percentiles=[5, 95])
