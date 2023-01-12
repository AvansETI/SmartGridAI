import uuid
from copy import copy

import matplotlib
import numpy as np
import pandas as pd
import shap
from flask import Flask, request, jsonify
from flask_cors import CORS
from sklearn.ensemble import ExtraTreesClassifier
from sklearn.feature_selection import SelectFwe, f_classif
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import MultinomialNB
from sklearn.neural_network import MLPClassifier
from sklearn.pipeline import make_pipeline, make_union
from sklearn.preprocessing import FunctionTransformer
from tpot.builtins import StackingEstimator
from tpot.builtins import ZeroCount

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
    features = tpot_data[['Thermal Preference', 'Temperature', 'Humidity', 'Mood', 'Mode Of Transport', 'Eat Recent_Two hours ago', 'Light', 'TVOC', 'Cloth 2', 'RMSSD']]
    training_features, testing_features, training_target, testing_target = \
        train_test_split(features, tpot_data['Thermal Comfort'], random_state=None)

    # Average CV score on the training set was: 0.6923169993950392
    exported_pipeline = make_pipeline(
        make_union(
            StackingEstimator(estimator=make_pipeline(
                SelectFwe(score_func=f_classif, alpha=0.048),
                StackingEstimator(estimator=MLPClassifier(alpha=0.01, learning_rate_init=0.001)),
                ZeroCount(),
                MultinomialNB(alpha=0.1, fit_prior=False)
            )),
            FunctionTransformer(copy)
        ),
        ExtraTreesClassifier(bootstrap=False, criterion="entropy", max_features=0.8, min_samples_leaf=3,
                             min_samples_split=8, n_estimators=100)
    )

    return exported_pipeline.fit(training_features, training_target), features


# The setup method is used for setting up everything that we need to work with.
def setup():
    # Load model.
    # Model has not yet been created. Pass it through the
    # load_model method once it has been created.
    _model, train_features = load_model()

    # Load SHAP (Explainability AI)
    _shap_explainer = shap.KernelExplainer(_model.predict_proba, train_features[:100])

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
        x = np.zeros((1, 10))

        x[0, 0] = content['thermalPreference']
        x[0, 1] = content['temperature']
        x[0, 2] = content['humidity']
        x[0, 3] = content['mood']
        x[0, 4] = content['modeOfTransport']
        x[0, 5] = content['eatRecentTwoHoursAgo']
        x[0, 6] = content['light']
        x[0, 7] = content['TVOC']
        x[0, 8] = content['cloth2']
        x[0, 9] = content['RMSSD']

        # Prediction
        prediction = model.predict(x)
        print(prediction)

        # # Explanation
        # shap_values = shap_explainer.shap_values(x)
        # shap_plot = shap.force_plot(
        #     shap_explainer.expected_value,
        #     shap_values[0],
        #     x,
        #     matplotlib=True,
        #     feature_names=['thermalPreference', 'temperatureF', 'humdity', 'mood', 'modeOfTransport', 'eatRecentTwoHoursAgo', 'light', 'TVOC', 'cloth2'],
        #     show=False,
        #     plot_cmap=['#77dd77', '#f99191']
        # )

        # # Encode shap img into base64,
        # buf = BytesIO()
        # plt.savefig(buf, format='png', bbox_inches="tight", transparent=True)
        # shap_img = base64.b64encode(buf.getvalue()).decode("utf-8").replace("\n", "")

        # Request response
        response = {
            "id": str(uuid.uuid4()),
            "thermalComfort": prediction[0],
            # "shap-img": shap_img,
            "errors": errors
        }
    else:
        # Return errors
        response = {"id": str(uuid.uuid4()), "errors": errors}

    return jsonify(response)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5045, debug=False)
