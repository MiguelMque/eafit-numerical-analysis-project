from interpolML.model import Model
from neuralprophet import NeuralProphet


class NeuralProphet(Model):
    """Constructor class to build a Neural Prophet model.

    """

    def __new__(cls, name: str) -> Model:
        model = cls._build_model()
        return model

    @classmethod
    def _build_model(cls):
        model = NeuralProphet()
        return model
