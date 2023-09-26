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