import numpy as np
import pandas as pd
from sklearn.ensemble import ExtraTreesClassifier
from sklearn.feature_selection import SelectFwe, f_classif
from sklearn.model_selection import train_test_split
from sklearn.pipeline import make_pipeline, make_union
from sklearn.preprocessing import PolynomialFeatures
from sklearn.tree import DecisionTreeClassifier
from tpot.builtins import StackingEstimator
from sklearn.preprocessing import FunctionTransformer
from copy import copy

# NOTE: Make sure that the outcome column is labeled 'target' in the data file
# Thermal Preference, TemperatureF, Humidity, Mood, Mode Of Transport, Eat Recent_Two hours ago, Light, TVOC, Cloth 2
tpot_data = pd.read_csv('PATH/TO/DATA/FILE', sep='COLUMN_SEPARATOR', dtype=np.float64)
features = tpot_data.drop('target', axis=1)
training_features, testing_features, training_target, testing_target = \
            train_test_split(features, tpot_data['target'], random_state=None)

# Average CV score on the training set was: 0.6819721718088324
exported_pipeline = make_pipeline(
    make_union(
        make_pipeline(
            PolynomialFeatures(degree=2, include_bias=False, interaction_only=False),
            SelectFwe(score_func=f_classif, alpha=0.022)
        ),
        FunctionTransformer(copy)
    ),
    StackingEstimator(estimator=DecisionTreeClassifier(criterion="gini", max_depth=3, min_samples_leaf=5, min_samples_split=20)),
    ExtraTreesClassifier(bootstrap=False, criterion="entropy", max_features=0.45, min_samples_leaf=3, min_samples_split=5, n_estimators=100)
)

exported_pipeline.fit(training_features, training_target)
results = exported_pipeline.predict(testing_features)
