from flask import jsonify
from handler.abstract_client_handler import AbstractClientHandler


class EditedClientLoanHandler(AbstractClientHandler):

    def __init__(self, client_id: int, request):
        super().__init__(client_id)
        self.request = request

    def edit_client(self, client):
        print("edit client")
        client_update = map_client_update(self.request)
        for column, value in client_update.items():
            client.loc[client.index[0], column] = value
        return client

    def route(self):
        try:
            if self.is_a_client():
                client = self.get_client()
                client = edit_client(client)
                return_dict = {
                    'prediction': self.get_prediction(client),
                    'probabilities': self.get_probabilities(client)
                }
                return jsonify(return_dict), 200
            else:
                return jsonify({"error": "Client forbidden"}), 403
        except Exception as e:
            return jsonify({"error": f"An error occurred{e}"}), 500
