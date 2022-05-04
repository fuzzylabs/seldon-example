
import joblib


class Model:
    def __init__(self):
        self._model = joblib.load("model.joblib")

    def predict(self, X):
        return self._model([X["sepal_length"], X["sepal_width"], X["petal_length"], X["petal_width"]])
