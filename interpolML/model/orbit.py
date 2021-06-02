from interpolML.model import Model
from orbit.models.dlt import DLTFull


class Orbit(Model):

    def __new__(cls) -> Model:
        model = cls._build_model()
        return model

    @classmethod
    def _build_model(cls):
        model = DLTFull(
            response_col='Claim', date_col='ds',
            seasonality=52,
        )

        return model
