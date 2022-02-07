import os
import shap
import pandas as pd
from cloudpickle import cloudpickle


class Predictor:
    def predict_model(self, data):
        """
        Uses the model and input data to predict satisfaction
        Args:
            data: Input array of data to predict satisfaction, must be in the same order as the features.csv file

        Returns:
            A basic prediction of satisfaction
        """
        return self.load_model().predict(data)[0]

    def predict_model_proba(self, data):
        """
        Uses the model and input data to predict satisfaction and return the probability
        Args:
            data: Input array of data to predict satisfaction, must be in the same order as the features.csv file

        Returns:
            A json with the basic prediction of satisfaction and the probability of that prediction
        """
        prediction = self.load_model().predict(data)[0]
        proba = self.load_model().predict_proba(data)[0]
        return {
            "satisfaction": prediction,
            "probability": proba[0] if (prediction < 1) else proba[1],
        }

    def load_model(self, filename="model.pkl"):
        with open(
            f"{os.path.dirname(os.path.abspath(__file__))}/{filename}", "rb"
        ) as file:
            model = cloudpickle.load(file)

            return model

    def plot(self, data):
        """
        Uses the shap explainer to return the shap plot for the input data
        Args:
            data: Input array of data to predict satisfaction, must be in the same order as the features.csv file

        Returns:
            A json with the shap plot data
        """
        df = pd.read_csv(f"{os.path.dirname(os.path.abspath(__file__))}/features.csv")
        X_train = pd.read_csv(
            f"{os.path.dirname(os.path.abspath(__file__))}/dataset.csv"
        )
        feature_names = df["features"]

        model = self.load_model()

        explainer = shap.KernelExplainer(model.predict_proba, shap.kmeans(X_train, 5))

        shap_values = explainer.shap_values(data)

        return shap.plots.force(
            explainer.expected_value[0],
            shap_values[0],
            data,
            plot_cmap=["#ff0d57", "#008000"],
            feature_names=feature_names,
        )

    def get_model_steps(self):
        """
        Gets the top n steps from the model
        Returns:
            Dictionary of the top n steps with parameters
        """
        model = self.load_model()

        steps = {}

        if type(model).__name__ == "Pipeline":
            for i in model.named_steps:
                steps[i] = model[i].get_params()
        else:
            steps[type(model).__name__] = model.get_params()

        return steps
