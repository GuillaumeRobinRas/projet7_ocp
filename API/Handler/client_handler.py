import pandas as pd
from flask import jsonify, request

from env import lgb_model_path, df_path
from utils.utils import load_model


model_lgb = load_model(lgb_model_path)
df = pd.read_csv(df_path)


def is_a_client(client_id: int) -> bool:
    if client_id in df['SK_ID_CURR'].tolist():
        return True
    else:
        return False


def get_client(client_id: int) -> pd.DataFrame:
    client = df[df['SK_ID_CURR'] == int(client_id)]
    client = client.iloc[:, 1:750]  # ligne à check car c'est un hotfix bizarre
    return client


def get_prediction(client: pd.DataFrame) -> list:
    prediction = model_lgb.predict(client)
    return prediction.tolist()


def get_probabilities(client: pd.DataFrame) -> list:
    probabilities = model_lgb.predict_proba(client)
    return probabilities.tolist()


def get_loan_risky(client_id: int):
    try:
        if is_a_client(client_id):
            client = get_client(client_id)
            return_dict = {
                'prediction': get_prediction(client),
                'probabilities': get_probabilities(client)
            }
            return jsonify(return_dict), 200
        else:
            return jsonify({"error": "Client forbidden"}), 403
    except Exception as e:
        return jsonify({"error": f"An error occurred{e}"}), 500


def edit_client(client, request):
    client.loc[client.index[0], 'AMT_CREDIT'] = float(request.args.get('loan_amount'))
    client.loc[client.index[0], 'DAYS_BIRTH'] = float(request.args.get('age'))
    client.loc[client.index[0], 'AMT_INCOME_TOTAL'] = float(request.args.get('income'))
    client.loc[client.index[0], 'AMT_ANNUITY'] = float(request.args.get('loan_duration_months'))
    client.loc[client.index[0], 'CODE_GENDER'] = float(request.args.get('gender'))
    return client


def get_loan_risky_for_custom_client(client_id):
    try:
        if is_a_client(client_id):
            client = get_client(client_id)
            client = edit_client(client, request)
            return_dict = {
                'prediction': get_prediction(client),
                'probabilities': get_probabilities(client)
            }
            return jsonify(return_dict), 200
        else:
            return jsonify({"error": "Client forbidden"}), 403
    except Exception as e:
        return jsonify({"error": f"An error occurred{e}"}), 500
