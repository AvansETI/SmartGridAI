import os
import joblib


class Predictor:
    def __init__(self):
        self.model = self.load_model()

    def predict_model(self, data):
        return self.model.predict(data)[0]

    def load_model(self, filename='model.sav'):
        return joblib.load(filename=f"{ os.path.dirname(os.path.abspath(__file__)) }/{ filename }")
