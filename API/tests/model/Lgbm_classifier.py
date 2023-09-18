import re
import gc
import numpy as np
import pandas as pd
from sklearn.model_selection import KFold
from sklearn.impute import SimpleImputer
from sklearn.metrics import make_scorer
from lightgbm import LGBMClassifier
import pickle


def split_ds(df):
    df = df.rename(columns=lambda x: re.sub('[^A-Za-z0-9_]+', '', x))
    # Divide in training/validation and test data
    train_df = df[df['TARGET'].notnull()]
    test_df = df[df['TARGET'].isnull()]
    print("Starting  model. Train shape: {}, test shape: {}".format(train_df.shape, test_df.shape))
    del df
    gc.collect()
    oof_preds = np.zeros(train_df.shape[0])
    sub_preds = np.zeros(test_df.shape[0])
    feature_importance_df = pd.DataFrame()
    folds = KFold(n_splits=4, shuffle=True, random_state=1001)
    feats = [f for f in train_df.columns if f not in ['TARGET', 'SK_ID_CURR', 'SK_ID_BUREAU', 'SK_ID_PREV', 'index']]
    for n_fold, (train_idx, valid_idx) in enumerate(folds.split(train_df[feats], train_df['TARGET'])):
        train_x, train_y = train_df[feats].iloc[train_idx], train_df['TARGET'].iloc[train_idx]
        valid_x, valid_y = train_df[feats].iloc[valid_idx], train_df['TARGET'].iloc[valid_idx]
    valid_x.to_csv('valid_x.csv')
    return train_x, train_y, valid_x, valid_y, oof_preds, sub_preds, feature_importance_df


def custom_metric(y_true, y_pred):
    fp = np.sum((y_true == 0) & (y_pred == 1))
    fn = np.sum((y_true == 1) & (y_pred == 0))
    tp = np.sum((y_true == 1) & (y_pred == 1))
    custom_score = fp * 10 + fn
    return custom_score


def preprocess_data():
    df = pd.read_csv("../tests_handler/dataset.csv")
    X_train, Y_train, X_valid, Y_valid, oof_preds, sub_preds, feature_importance_df = split_ds(df)
    imp_mean = SimpleImputer(strategy='mean')
    imp_mean.fit(X_train)
    X_train = imp_mean.transform(X_train)
    X_valid = imp_mean.transform(X_valid)
    return X_train, Y_train, X_valid, Y_valid, oof_preds, sub_preds, feature_importance_df


def train_model():
    X_train, Y_train, X_valid, Y_valid, oof_preds, sub_preds, feature_importance_df = preprocess_data()
    custom_scorer = make_scorer(custom_metric, greater_is_better=True)
    class_weights = {0: 1.0, 1: 1 / 0.0688}
    lgb_classifier = LGBMClassifier(class_weight=class_weights, random_state=42)
    lgb_classifier.fit(X_train, Y_train)
    return lgb_classifier


def save_model(name: str, model):
    with open(f'{name}.pkl', 'wb') as file:
        pickle.dump(model, file)


lgb = train_model()
save_model('lgb_classifier', lgb)
