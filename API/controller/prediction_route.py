from flask import Flask, request, Blueprint
from Handler import client_handler

prediction = Blueprint('prediction', __name__)


@prediction.route('/loan/<int:client_id>', methods=['GET'])
def get_loan_risky(client_id):
    return client_handler.get_loan_risky(client_id)


@prediction.route('/loan/custom/<int:client_id>', methods=['GET'])
def get_loan_risky_for_custom_client(client_id):
    return client_handler.get_loan_risky_for_custom_client(client_id, request)
