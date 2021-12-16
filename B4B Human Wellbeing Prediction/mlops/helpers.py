from datetime import datetime

import pandas as pd
from sklearn.metrics import roc_auc_score, recall_score, precision_score, log_loss, f1_score, \
    brier_score_loss, average_precision_score, accuracy_score, balanced_accuracy_score
from sklearn.model_selection import train_test_split


def default_file_name():
    return datetime.today().strftime('%d-%m-%Y_%H-%M-%S')


def get_data_and_split(file_path):
    df = pd.read_csv(file_path)[:1000]

    y = df['target']
    X = df.drop('target', axis=1)

    return train_test_split(X, y, stratify=y.values, test_size=0.33)


def custom_scoring(y_true, y_pred):
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

    return sum(scores.values())
