from interpolML.model import Model
import pandas as pd
from orbit.diagnostics.metrics import smape, wmape, mape, mse, mae
import numpy as np
from copy import deepcopy


class Metrics:
    _default_metrics = [smape, wmape, mape, mse, mae]

    def __init__(self, model: Model, df):
        self.model = deepcopy(model)
        self.data = df
        self._score_df = pd.DataFrame()
        self._test_actual = []
        self._test_predicted = []

    def _evaluate_test_metric(self, metric):

        response_col = self.model.y_col
        prediction = self.model.prediction.prediction

        self._test_actual = np.concatenate((self._test_actual, self.model.test[response_col].to_numpy()))
        self._test_predicted = np.concatenate((self._test_predicted, prediction.to_numpy()))
        eval_out = metric(actual=self._test_actual, predicted=self._test_predicted)

        return eval_out

    def score(self, metrics=None):
        if metrics is None:
            metrics = self._default_metrics

        eval_out_list = list()

        for metric in metrics:
            eval_out = self._evaluate_test_metric(metric)
            eval_out_list.append(eval_out)

        metrics_str = [x.__name__ for x in metrics]
        self._score_df = pd.DataFrame(metrics_str, columns=['metric_name'])
        self._score_df['metric_values'] = eval_out_list

        return self._score_df
