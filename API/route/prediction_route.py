from flask import Flask, request, Blueprint


@prediction.route('/loan/<int:client_id>', methods=['GET'])
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


@prediction.route('/loan/custom/<int:client_id>', methods=['GET'])
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