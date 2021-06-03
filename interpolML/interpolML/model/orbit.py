from interpolML.model import Model
from orbit.models.lgt import LGTFull


class Orbit(Model):

    def __new__(cls, name:str,freq:str) -> Model:
        model = cls._build_model()
        return Model(name=name, model=model, freq=freq)

    @classmethod
    def _build_model(cls):
        model = LGTFull(
            response_col="y",
            date_col="ds",
            seasonality=52,
        )

        return model
