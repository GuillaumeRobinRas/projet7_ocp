from flask import jsonify, request
import seaborn as sns
import matplotlib.pyplot as plt
import io


from ..Handler.abstract_client_handler import AbstractClientHandler


class BivariateAnalysisHandler(AbstractClientHandler):

    def __init__(self):
        super().__init__(int(request.args.get('client_id')))
        self.feature1 = request.args.get('feature1')
        self.feature2 = request.args.get('feature2')

    def make_graph(self):
        plt.figure(figsize=(10, 6))
        sns.boxplot(x=self.feature1, y=self.feature2, data=self.df)
        plt.title(f'Analyse bivariée de {self.feature1} et {self.feature2}')
        client_row = self.df[self.df['SK_ID_CURR'] == self.client_id]
        sns.scatterplot(x=client_row[self.feature1], y=client_row[self.feature2], color='red', marker='o')
        buffer = io.BytesIO()
        plt.savefig(buffer, format='png')
        buffer.seek(0)
        return buffer

    def route(self):
        try:
            if self.is_a_feature(self.feature1) and self.is_a_feature(self.feature2):
                buffer = self.make_graph()
                img = self.convert_to_base64(buffer)
                return jsonify({"image": img})
            else:
                return jsonify({"error": f"Feature '{feature1}' or '{feature2}' not found"}), 404
        except Exception as e:
            print(e)
            return jsonify({"error": "An error occurred"}), 500