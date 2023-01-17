import numpy as np
import pandas as pd
from sklearn.ensemble import ExtraTreesRegressor
from sklearn.feature_selection import VarianceThreshold
from sklearn.model_selection import train_test_split
from sklearn.pipeline import make_pipeline, make_union
from sklearn.preprocessing import MinMaxScaler, StandardScaler
from sklearn.svm import LinearSVR
from tpot.builtins import StackingEstimator

# NOTE: Make sure that the outcome column is labeled 'target' in the data file
# Thermal Preference, TemperatureF, Humidity, Mood, Mode Of Transport, Eat Recent_Two hours ago, Light, TVOC, Cloth 2
tpot_data = pd.read_csv('final.csv')
target = tpot_data['Thermal Comfort']
features = tpot_data[['Thermal Preference', 'Temperature', 'Humidity', 'Mood', 'Mode Of Transport', 'Eat Recent_Two hours ago', 'Light', 'TVOC', 'Cloth 2', 'RMSSD']]
training_features, testing_features, training_target, testing_target = \
            train_test_split(features, target, random_state=None)

# Average CV score on the training set was: -0.29205888082274656
exported_pipeline = make_pipeline(
    StackingEstimator(estimator=LinearSVR(C=0.01, dual=False, epsilon=0.1, loss="squared_epsilon_insensitive", tol=0.0001)),
    StandardScaler(),
    MinMaxScaler(),
    VarianceThreshold(threshold=0.01),
    MinMaxScaler(),
    ExtraTreesRegressor(bootstrap=False, max_features=0.4, min_samples_leaf=1, min_samples_split=3, n_estimators=100)
)

exported_pipeline.fit(training_features, training_target)
results = exported_pipeline.predict(testing_features)

print('Test:', exported_pipeline.score(testing_features, testing_target))
print('Train:', exported_pipeline.score(training_features, training_target))