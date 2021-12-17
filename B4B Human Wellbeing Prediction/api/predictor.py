import pandas as pd
import shap
from cloudpickle import cloudpickle


class Predictor:
    def __init__(self):
        self.model = self.load_model()

    def predict_model(self, data):
        return self.model.predict(data)[0]

    def load_model(self, filename='model.pkl'):
        with open(filename, "rb") as file:
            model = cloudpickle.load(file)

            return model

    def load_explainer(self, filename='explainer.pkl'):
        with open(filename, "rb") as file:
            explainer = cloudpickle.load(file)

            return explainer

    def plot(self, data):
        df = pd.read_csv('features.csv')
        feature_names = df['features']

        explainer = self.load_explainer()

        shap_values = explainer.shap_values(data)

        return shap.plots.force(explainer.expected_value[0], shap_values[0], data, plot_cmap=["#ff0d57", "#008000"],
                                feature_names=feature_names)
