from flask import jsonify, request
from handler.abstract_client_handler import AbstractClientHandler


class EditedClientLoanHandler(AbstractClientHandler):

    def __init__(self, client_id: int):
        super(client_id)
        self.request = request.args.to_dict()
        self.request_dict = self.dict_mapper()

    @property
    def dict_match(self):
        return {
            'AMT_CREDIT': 'loan_amount',
            'DAYS_BIRTH': 'age',
            'AMT_INCOME_TOTAL': 'income',
            'AMT_ANNUITY': 'loan_duration_months',
            'CODE_GENDER': 'gender'
        }

    def dict_mapper(self):
        result_dict = {}
        for key1, key2 in self.dict_match.items():
            if key2 in self.request:
                result_dict[key1] = self.request[key2]
        return result_dict

    def edit_client(self, client):
        for column, value in self.request_dict.items():
            client[[column]] = float(value)
        return client

    def route(self):
        try:
            if self.is_a_client():
                client = self.edit_client(self.get_client())
                return_dict = {
                    'prediction': self.get_prediction(client),
                    'probabilities': self.get_probabilities(client)
                }
                return jsonify(return_dict), 200
            else:
                return jsonify({"error": "Client forbidden"}), 403
        except Exception as e:
            return jsonify({"error": f"An error occurred{e}"}), 500
