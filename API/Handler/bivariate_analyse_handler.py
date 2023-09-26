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