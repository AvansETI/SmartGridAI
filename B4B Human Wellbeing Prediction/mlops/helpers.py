from datetime import datetime

import pandas as pd
from sklearn.metrics import roc_auc_score, recall_score, precision_score, log_loss, f1_score, \
    brier_score_loss, average_precision_score, accuracy_score, balanced_accuracy_score
from sklearn.model_selection import train_test_split


def default_file_name():
    return datetime.today().strftime('%d-%m-%Y_%H-%M-%S')


def get_data_and_split(file_path):
    df = pd.read_csv(file_path)

    y = df['target']
    X = df.drop('target', axis=1)

    return train_test_split(X, y, stratify=y.values, test_size=0.33, random_state=1)


# score will score the model based on a few different scoring functions and return it as a dictionary
def score(y_true, y_pred):
    accuracy = accuracy_score(y_true, y_pred)
    balanced_accuracy = balanced_accuracy_score(y_true, y_pred)
    average_precision = average_precision_score(y_true, y_pred)
    neg_brier_score = 1 - brier_score_loss(y_true, y_pred)
    f1 = f1_score(y_true, y_pred)
    neg_log_loss = 1 - log_loss(y_true, y_pred)
    precision = precision_score(y_true, y_pred)
    recall = recall_score(y_true, y_pred)
    roc_auc = roc_auc_score(y_true, y_pred)

    scores = {
        'accuracy': accuracy,
        'balanced_accuracy': balanced_accuracy,
        'average_precision': average_precision,
        'neg_brier_score': neg_brier_score,
        'f1': f1,
        'neg_log_loss': neg_log_loss,
        'precision': precision,
        'recall': recall,
        'roc_auc': roc_auc,
    }

    [print(name, score) for name, score in scores.items()]

    print(f'total {sum(scores.values())}\n')

    return scores


# custom_scoring gets the values from the score function and simply returns the sum of the scores
# custom_scoring and score are split up because score can now be used to get the scores separately if needed while
# custom_scoring can be used to only get the sum score which is needed for the tpot optimizer
def custom_scoring(y_true, y_pred):
    return sum(score(y_true, y_pred).values())


# custom_scoring_threshold gets the scores from the score function and checks if they passed a number of thresholds
# For every score a threshold can be entered which can be found in the score_thresholds dictionary
# There is also a mean_score_threshold which is used to check the mean of all scores
def custom_scoring_threshold(model, X_test, y_test):
    mean_score_threshold = 0.9

    score_thresholds = {
        'accuracy': 0.9,
        'balanced_accuracy': 0.9,
        'average_precision': 0.9,
        'neg_brier_score': 0.9,
        'f1': 0.9,
        'neg_log_loss': 0.9,
        'precision': 0.9,
        'recall': 0.9,
        'roc_auc': 0.9,
    }

    predictions = model.predict(X_test)

    scores = score(predictions, y_test)
    total_score = sum(scores.values())

    if total_score < mean_score_threshold * len(scores):
        return False

    for key, value in score_thresholds.items():
        if scores[key] < value:
            return False

    return True
