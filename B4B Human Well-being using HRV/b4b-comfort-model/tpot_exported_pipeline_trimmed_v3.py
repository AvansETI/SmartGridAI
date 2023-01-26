import numpy as np
import pandas as pd
from sklearn.ensemble import ExtraTreesClassifier
from sklearn.feature_selection import SelectFwe, f_classif
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import MultinomialNB
from sklearn.neural_network import MLPClassifier
from sklearn.pipeline import make_pipeline, make_union
from tpot.builtins import StackingEstimator, ZeroCount
from sklearn.preprocessing import FunctionTransformer
from copy import copy

# NOTE: Make sure that the outcome column is labeled 'target' in the data file
# Thermal Preference, Temperature, Humidity, Mood, Mode Of Transport, Eat Recent_Two hours ago, Light, TVOC, Cloth 2, RMSSD
tpot_data = pd.read_csv('final.csv')
target = tpot_data['Thermal Comfort']
features = tpot_data[['Thermal Preference', 'Temperature', 'Humidity', 'Mood', 'Mode Of Transport', 'Eat Recent_Two hours ago', 'Light', 'TVOC', 'Cloth 2', 'RMSSD']]
training_features, testing_features, training_target, testing_target = \
            train_test_split(features, target, random_state=None)

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
    ExtraTreesClassifier(bootstrap=False, criterion="entropy", max_features=0.8, min_samples_leaf=3, min_samples_split=8, n_estimators=100)
)

exported_pipeline.fit(training_features, training_target)
results = exported_pipeline.predict(testing_features)

print('Test:', exported_pipeline.score(testing_features, testing_target))
print('Train:', exported_pipeline.score(training_features, training_target))
