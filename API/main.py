from flask import Flask, jsonify, request
from env import lgb_model_path
from utils import load_model
import json
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import io
import base64
import numpy as np
from PIL import Image

app = Flask(__name__)
model_lgb = load_model(lgb_model_path)
df = pd.read_csv('../dataset.csv')


@app.route('/loan/<int:client_id>', methods=['GET'])
def get_loan_risky(client_id):
    try:
        if client_id in df['SK_ID_CURR'].tolist():
            client = df[df['SK_ID_CURR'] == int(client_id)]
            client = client.iloc[:, 1:750]
            prediction = model_lgb.predict(client)
            probabilities = model_lgb.predict_proba(client)
            return_dict = {
                'prediction': prediction.tolist(),
                'probabilities': probabilities.tolist()
            }
            return jsonify(return_dict)
        else:
            return jsonify({"error": "Client forbidden"}), 403
    except Exception as e:
        print(e)
        return jsonify({"error": "An error occurred"}), 500


@app.route('/loan/custom/<int:client_id>', methods=['GET'])
def get_loan_risky_for_custom_client(client_id):
    try:
        if client_id in df['SK_ID_CURR'].tolist():
            client = df[df['SK_ID_CURR'] == int(client_id)]
            client = client.iloc[:, 1:750]
            client.loc[client.index[0], 'AMT_CREDIT'] = float(request.args.get('loan_amount'))
            client.loc[client.index[0], 'DAYS_BIRTH'] = float(request.args.get('age'))
            client.loc[client.index[0], 'AMT_INCOME_TOTAL'] = float(request.args.get('income'))
            client.loc[client.index[0], 'AMT_ANNUITY'] = float(request.args.get('loan_duration_months'))
            client.loc[client.index[0], 'CODE_GENDER'] = float(request.args.get('gender'))
            prediction = model_lgb.predict(client)
            probabilities = model_lgb.predict_proba(client)
            return_dict = {
                'prediction': prediction.tolist(),
                'probabilities': probabilities.tolist()
            }
            return jsonify(return_dict)
        else:
            return jsonify({"error": "Client not forbidden"}), 403
    except Exception as e:
        print(e)
        return jsonify({"error": "An error occurred"}), 500


@app.route('/loan/bivariate/', methods=['GET'])
def bivariate_analysis():
    try:
        feature1 = request.args.get('feature1')
        feature2 = request.args.get('feature2')
        client_id = int(request.args.get('client_id'))

        if feature1 in df.columns and feature2 in df.columns:
            plt.figure(figsize=(10, 6))
            sns.boxplot(x=feature1, y=feature2, data=df)
            plt.title(f'Analyse bivariée de {feature1} et {feature2}')

            client_row = df[df['SK_ID_CURR'] == client_id]
            sns.scatterplot(x=client_row[feature1], y=client_row[feature2], color='red', marker='o')

            # Sauvegarder le graphique dans un buffer
            buffer = io.BytesIO()
            plt.savefig(buffer, format='png')
            buffer.seek(0)

            # Convertir le graphique en base64 pour le renvoyer dans la réponse
            image_base64 = base64.b64encode(buffer.read()).decode('utf-8')

            return jsonify({"image": image_base64})
        else:
            return jsonify({"error": f"Feature '{feature1}' or '{feature2}' not found"}), 404
    except Exception as e:
        print(e)
        return jsonify({"error": "An error occurred"}), 500


@app.route('/loan/feature_importance/<int:client_id>', methods=['GET'])
def feature_importance(client_id):
    try:
        if client_id in df['SK_ID_CURR'].tolist():
            client = df[df['SK_ID_CURR'] == int(client_id)]
            client = client.iloc[:, :749]  # Assurez-vous de sélectionner les bonnes colonnes

            booster = model_lgb.booster_
            importance = booster.feature_importance(importance_type='split')
            feature_names = booster.feature_name()

            client_importance = importance * client.values[0]

            client_importance_dict = {}
            for i, importance_value in enumerate(client_importance):
                column_name = df.columns[i + 1]  # +1 pour sauter la colonne 'SK_ID_CURR'
                client_importance_dict[column_name] = {
                    "importance": importance_value,
                    "column_name": column_name
                }

            sorted_importance = sorted(client_importance_dict.values(), key=lambda item: item["importance"], reverse=True)

            return jsonify(sorted_importance)
        else:
            return jsonify({"error": "Client not found"}), 404
    except Exception as e:
        print(e)
        return jsonify({"error": "An error occurred"}), 500


@app.route('/loan/distribution/<int:client_id>/<feature_name>', methods=['GET'])
def feature_distribution(client_id, feature_name):
    try:
        if client_id in df['SK_ID_CURR'].tolist() and feature_name in df.columns:
            client = df[df['SK_ID_CURR'] == int(client_id)]
            client_feature_value = client[feature_name].values[0]

            plt.figure(figsize=(10, 6))
            sns.histplot(data=df, x=feature_name, hue='TARGET', multiple='stack', kde=True)
            plt.title(f'Distribution de la fonctionnalité {feature_name} en fonction de la classe')

            plt.axvline(x=client_feature_value, color='red', linestyle='dashed', label='Client')
            plt.legend()

            # Sauvegarder le graphique dans un buffer
            buffer = io.BytesIO()
            plt.savefig(buffer, format='png')
            buffer.seek(0)

            # Convertir le graphique en base64 pour le renvoyer dans la réponse
            image_base64 = base64.b64encode(buffer.read()).decode('utf-8')

            return jsonify({"image": image_base64})
        else:
            return jsonify({"error": "Client or feature not found"}), 404
    except Exception as e:
        print(e)
        return jsonify({"error": "An error occurred"}), 500


if __name__ == '__main__':
    app.run(debug=True)


