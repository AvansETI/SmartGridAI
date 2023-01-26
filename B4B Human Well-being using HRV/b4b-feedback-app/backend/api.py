import base64
import uuid
from io import BytesIO

import matplotlib
import numpy as np
import pandas as pd
import shap
from flask import Flask, request, jsonify
from flask_cors import CORS
from matplotlib import pyplot as plt
from sklearn.ensemble import ExtraTreesRegressor
from sklearn.feature_selection import VarianceThreshold
from sklearn.model_selection import train_test_split
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import MinMaxScaler, StandardScaler
from sklearn.svm import LinearSVR
from tpot.builtins import StackingEstimator

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
    features = tpot_data[
        ['Thermal Preference', 'Temperature', 'Humidity', 'Mood', 'Mode Of Transport', 'Eat Recent_Two hours ago',
         'Light', 'TVOC', 'Cloth 2', 'RMSSD']]
    target = tpot_data['Thermal Comfort']
    training_features, testing_features, training_target, testing_target = \
        train_test_split(features.values, target.values, random_state=None)

    # Average CV score on the training set was: -0.29205888082274656
    exported_pipeline = make_pipeline(
        StackingEstimator(
            estimator=LinearSVR(C=0.01, dual=False, epsilon=0.1, loss="squared_epsilon_insensitive", tol=0.0001)),
        StandardScaler(),
        MinMaxScaler(),
        VarianceThreshold(threshold=0.01),
        MinMaxScaler(),
        ExtraTreesRegressor(bootstrap=False, max_features=0.4, min_samples_leaf=1, min_samples_split=3,
                            n_estimators=100)
    )

    exported_pipeline.fit(training_features, training_target)

    return exported_pipeline

    # shap_df = pd.DataFrame(exported_pipeline.named_steps['minmaxscaler-2'].transform(
    #     exported_pipeline.named_steps['variancethreshold'].transform(
    #         exported_pipeline.named_steps['minmaxscaler-1'].transform(
    #             exported_pipeline.named_steps['standardscaler'].transform(
    #                 exported_pipeline.named_steps['stackingestimator'].transform(training_features[:100]))))))
    #
    # _shap_explainer = shap.KernelExplainer(exported_pipeline.named_steps['extratreesregressor'].predict,
    #                                        shap_df)
    #
    # return exported_pipeline, _shap_explainer, shap_df


# The setup method is used for setting up everything that we need to work with.
def setup():
    # Load model.
    # Model has not yet been created. Pass it through the
    # load_model method once it has been created.
    _model = load_model()

    return _model

    # _model, _shap_explainer, shap_df = load_model()
    # return _model, _shap_explainer, shap_df



model = setup()
# model, shap_explainer, shap_data = setup()


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
        # shap_values = shap_explainer.shap_values(shap_data)
        # shap_plot = shap.force_plot(
        #     shap_explainer.expected_value,
        #     shap_values[0],
        #     x,
        #     matplotlib=True,
        #     feature_names=['thermalPreference', 'temperature', 'humdity', 'mood', 'modeOfTransport',
        #                    'eatRecentTwoHoursAgo', 'light', 'TVOC', 'cloth2', 'RMSSD'],
        #     show=False,
        #     plot_cmap=['#77dd77', '#f99191']
        # )
        #
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
