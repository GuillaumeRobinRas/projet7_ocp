from flask import Flask, request, Blueprint


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
            return jsonify({"error": f"Feature '{feature1}' or '{feature2}' not found"})
    except Exception as e:
        print(e)
        return jsonify({"error": "An error occurred"})


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
            return jsonify({"error": "Client not found"})
    except Exception as e:
        print(e)
        return jsonify({"error": "An error occurred"})


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
            return jsonify({"error": "Client or feature not found"})
    except Exception as e:
        print(e)
        return jsonify({"error": "An error occurred"})
