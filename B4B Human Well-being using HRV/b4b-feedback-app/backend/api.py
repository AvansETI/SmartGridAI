import uuid
import numpy as np
import shap
import base64

import pandas as pd

from flask import Flask, request, jsonify
# from keras.models import load_model
from sklearn.model_selection import train_test_split
from io import BytesIO
from flask_cors import CORS
import numpy as np
import pandas as pd
from sklearn.ensemble import ExtraTreesClassifier
from sklearn.feature_selection import RFE
from sklearn.linear_model import SGDClassifier
from sklearn.model_selection import train_test_split
from sklearn.pipeline import make_pipeline, make_union
from sklearn.preprocessing import MinMaxScaler
from sklearn.tree import DecisionTreeClassifier
from tpot.builtins import StackingEstimator

import matplotlib
import matplotlib.pyplot as plt

matplotlib.use('Agg')

app = Flask(__name__)
# Solves Cross Origin Resource Sharing (CORS)
CORS(app)

# Used for validation
EXPECTED = {
    # Expected fields with potential constrains go here.
}


# This method is used for data transformation.
def transform_data(df):
    return df


# This method is used for loading the needed data.
def load_model():
    tpot_data = pd.read_csv('stripped.csv')
    features = tpot_data.drop('Thermal Comfort', axis=1)
    training_features, testing_features, training_target, testing_target = \
        train_test_split(features, tpot_data['Thermal Comfort'], random_state=None)

    # Average CV score on the training set was: 0.7111917725347852
    exported_pipeline = make_pipeline(
        StackingEstimator(
            estimator=SGDClassifier(alpha=0.0, eta0=0.1, fit_intercept=False, l1_ratio=0.0, learning_rate="invscaling",
                                    loss="modified_huber", penalty="elasticnet", power_t=100.0)),
        MinMaxScaler(),
        RFE(estimator=ExtraTreesClassifier(criterion="entropy", max_features=0.05, n_estimators=100),
            step=0.6000000000000001),
        DecisionTreeClassifier(criterion="entropy", max_depth=5, min_samples_leaf=3, min_samples_split=8)
    )

    return exported_pipeline.fit(training_features, training_target), features


# The setup method is used for setting up everything that we need to work with.
def setup():
    # Load model.
    # Model has not yet been created. Pass it through the
    # load_model method once it has been created.
    _model, train_features = load_model()

    # Load training data.
    # (train_features, _), _ = load_data()

    # Load SHAP (Explainability AI)
    _shap_explainer = shap.KernelExplainer(_model.predict_proba, train_features[:100])

    # _shap_explainer = shap.KernelExplainer(_model, train_features[:100])

    return _model, _shap_explainer


model, shap_explainer = setup()


@app.route('/', methods=['GET'])
def root():
    response = {
        "author": "Job Haast, Niek Snijders, Noah Korten, Stefan Jaspers",
        "description": "API for B4B Feedback Application",
        "version": "1.0"
    }
    return jsonify(response)


@app.route('/api/predict', methods=['POST'])
def predict():
    content = request.json
    errors = []

    # # Check for valid input fields
    # for name in content:
    #     if name in EXPECTED:
    #         expected_min = EXPECTED[name]['min']
    #         expected_max = EXPECTED[name]['max']
    #         value = float(content[name])
    #         if value < expected_min or value > expected_max:
    #             errors.append(
    #                 f"Out of bounds: {name}, has value of: {value}, but should be between {expected_min} and {expected_max}."
    #             )
    #     else:
    #         errors.append(f"Unexpected field: {name}.")

    # Check for missing input fields
    for name in EXPECTED:
        if name not in content:
            errors.append(f"Missing value: {name}.")

    if len(errors) < 1:
        # Predict
        x = np.zeros((1, 6))

        x[0, 0] = content['decile3']
        x[0, 1] = content['decile1']
        x[0, 2] = content['lsat']
        x[0, 3] = content['ugpa']
        x[0, 4] = content['fulltime']
        x[0, 5] = content['grad']

        # Prediction
        prediction = model.predict(x)

        # Explanation
        shap_values = shap_explainer.shap_values(x)
        shap_plot = shap.force_plot(
            shap_explainer.expected_value,
            shap_values[0],
            x,
            matplotlib=True,
            feature_names=['Decile3', 'Decile1', 'lsat', 'ugpa', 'fulltime', 'grad'],
            show=False,
            plot_cmap=['#77dd77', '#f99191']
        )

        # Encode shap img into base64,
        buf = BytesIO()
        plt.savefig(buf, format='png', bbox_inches="tight", transparent=True)
        shap_img = base64.b64encode(buf.getvalue()).decode("utf-8").replace("\n", "")

        # Request response
        response = {
            "id": str(uuid.uuid4()),
            "thermalComfort": prediction,
            "shap-img": shap_img,
            "errors": errors
        }
    else:
        # Return errors
        response = {"id": str(uuid.uuid4()), "errors": errors}

    return jsonify(response)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5045, debug=False)
