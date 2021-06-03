from interpolML.model import Model
from neuralprophet import NeuralProphet


class NProphet(Model):
    """Constructor class to build a Neural Prophet model.

    """

    def __new__(cls, name:str, freq:str) -> Model:
        model = cls._build_model()
        return Model(name=name, model=model, freq=freq)

    @classmethod
    def _build_model(cls):
        model = NeuralProphet()
        return model
