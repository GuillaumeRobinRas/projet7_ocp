import unittest
import pandas as pd
from unittest.mock import patch, Mock
from ..handler.abstract_client_handler import AbstractClientHandler


class TestAbstractClientHandler(unittest.TestCase):
    def setUp(self):
        # Créez un client fictif pour les tests
        self.client_id = 12345
        self.handler = AbstractClientHandler(self.client_id)

    def test_is_a_client_true(self):
        # Testez le cas où le client existe dans le DataFrame
        with patch.object(pd.DataFrame, 'tolist', return_value=[12345]):
            self.assertTrue(self.handler.is_a_client())

    def test_is_a_client_false(self):
        # Testez le cas où le client n'existe pas dans le DataFrame
        with patch.object(pd.DataFrame, 'tolist', return_value=[67890]):
            self.assertFalse(self.handler.is_a_client())

    @patch('your_module.load_model')
    def test_get_prediction(self, mock_load_model):
        # Mockez la méthode load_model pour éviter de charger un vrai modèle
        mock_load_model.return_value = Mock(predict=Mock(return_value=[0.75]))

        # Créez un client fictif pour les tests
        client = pd.DataFrame({'feature_1': [0.1], 'feature_2': [0.2]})

        prediction = self.handler.get_prediction(client)
        self.assertEqual(prediction, [0.75])

    @patch('your_module.load_model')
    def test_get_probabilities(self, mock_load_model):
        # Mockez la méthode load_model pour éviter de charger un vrai modèle
        mock_load_model.return_value = Mock(predict_proba=Mock(return_value=[[0.2, 0.8]]))

        # Créez un client fictif pour les tests
        client = pd.DataFrame({'feature_1': [0.1], 'feature_2': [0.2]})

        probabilities = self.handler.get_probabilities(client)
        self.assertEqual(probabilities, [[0.2, 0.8]])


if __name__ == '__main__':
    unittest.main()
