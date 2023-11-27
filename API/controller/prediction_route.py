from flask import Flask, request, Blueprint
from Handler import client_loan_handler, edited_client_loan_handler

prediction = Blueprint('prediction', __name__)


@prediction.route('/loan/<int:client_id>', methods=['GET'])
def get_loan_risky(client_id):
    return client_loan_handler.ClientLoanHandler(client_id).route()


@prediction.route('/loan/custom/<int:client_id>', methods=['GET'])
def get_loan_risky_for_custom_client(client_id):
    return edited_client_loan_handler.EditedClientLoanHandler(client_id).route()



