from flask import jsonify
from handler.abstract_client_handler import AbstractClientHandler


class ClientLoanHandler(AbstractClientHandler):

    def __init__(self, client_id: int):
        super().__init__(client_id)

    def route(self):
        try:
            if self.is_a_client():
                client = self.get_client()
                return_dict = {
                    'prediction': self.get_prediction(client),
                    'probabilities': self.get_probabilities(client)
                }
                return jsonify(return_dict), 200
            else:
                return jsonify({"error": "Client forbidden"}), 403
        except Exception as e:
            return jsonify({"error": f"An error occurred{e}"}), 500
