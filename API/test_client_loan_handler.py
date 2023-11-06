import unittest
from unittest.mock import patch, Mock
from flask import jsonify, Flask
import json
from .Handler.abstract_client_handler import AbstractClientHandler
from .Handler.client_loan_handler import ClientLoanHandler


class TestClientLoanHandler(unittest.TestCase):
    def setUp(self):
        self.app = Flask(__name__)
        self.client_id = 12345
        self.handler = ClientLoanHandler(self.client_id)
        self.app_context = self.app.app_context()
        self.app_context.push()

    def tearDown(self):
        self.app_context.pop()

    @patch.object(ClientLoanHandler, 'is_a_client', return_value=True)
    @patch.object(ClientLoanHandler, 'get_client', return_value='mocked_client_data')
    @patch.object(ClientLoanHandler, 'get_prediction', return_value=[0.75])
    @patch.object(ClientLoanHandler, 'get_probabilities', return_value=[0.2, 0.8])
    def test_route_success(self, mock_get_probabilities, mock_get_prediction, mock_get_client, mock_is_a_client):
        resp, status_code = self.handler.route()
        mock_is_a_client.assert_called_once()
        mock_get_client.assert_called_once()
        mock_get_prediction.assert_called_once()
        mock_get_probabilities.assert_called_once()
        expected_response ='{"prediction":[0.75],"probabilities":[0.2,0.8]}\n'
        response = resp.get_data().decode("utf-8")
        self.assertEqual(status_code, 200)
        self.assertEqual(response, expected_response)

    @patch.object(ClientLoanHandler, 'is_a_client', return_value=False)
    def test_route_client_forbidden(self, mock_is_a_client):
        resp, status_code = self.handler.route()
        mock_is_a_client.assert_called_once()
        response = resp.get_data().decode("utf-8")
        expected_response = '{"error":"Client forbidden"}\n'
        self.assertEqual(response, expected_response)
        self.assertEqual(status_code, 403)

    @patch.object(ClientLoanHandler, 'is_a_client', side_effect=Exception('Test error'))
    def test_route_exception(self, mock_is_a_client):
        resp, status_code = self.handler.route()
        mock_is_a_client.assert_called_once()
        response = resp.get_data().decode("utf-8")
        expected_response = '{"error":"An error occurredTest error"}\n'
        self.assertEqual(response, expected_response)
        self.assertEqual(status_code, 500)


if __name__ == '__main__':
    unittest.main()
