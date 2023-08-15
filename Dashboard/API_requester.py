import requests
from ENV import API_URL
from PIL import Image
import base64
import io


class APIRequester:
    def __init__(self):
        self.api_url = API_URL

    @staticmethod
    def loan_probabilities_call(identity: int) -> dict:
        url = API_URL + "loan/" + str(identity)
        try:
            response = requests.get(url)
            response.raise_for_status()
            json_data = response.json()
            return json_data
        except requests.exceptions.RequestException as e:
            print(f"Une erreur s'est produite lors de l'appel API : {e}")

    def loan_probabilities_custom_client(self, client_id, loan_amount, age, income, loan_duration_months, gender) -> dict:
        url = self.api_url + "loan/custom/" + str(client_id)
        params = {
            'loan_amount': loan_amount,
            'age': age,
            'income': income,
            'loan_duration_months': loan_duration_months,
            'gender': gender
        }
        try:
            response = requests.get(url, params=params)
            json_data = response.json()
            return json_data

        except requests.exceptions.RequestException as e:
            print("Erreur de connexion à l'API :", e)
        except Exception as e:
            print("Une erreur est survenue :", e)

    def bivariate_analysis(self, customer_id, feature1, feature2) -> dict:
        url = self.api_url + "loan/bivariate"
        params = {
            'client_id': customer_id,
            'feature1': feature1,
            'feature2': feature2
        }
        try:
            response = requests.get(url, params=params)
            response.raise_for_status()
            json_data = response.json()
            return json_data
        except requests.exceptions.RequestException as e:
            print(f"Une erreur s'est produite lors de l'appel API : {e}")

    def client_features_importance_call(self,identity: int) -> list:
        url = self.api_url + "loan/feature_importance/" + str(identity)
        try:
            response = requests.get(url)
            response.raise_for_status()
            json_data = response.json()
            return json_data
        except requests.exceptions.RequestException as e:
            print(f"Une erreur s'est produite lors de l'appel API : {e}")

    def feature_distribution(self, client_id: int, feature_name: str) -> Image:
        try:
            url = f"{self.api_url}loan/distribution/{client_id}/{feature_name}"
            response = requests.get(url)
            response_data = response.json()

            if "image" in response_data:
                image_base64 = response_data["image"]
                image_bytes = base64.b64decode(image_base64)
                return Image.open(io.BytesIO(image_bytes))
            else:
                print("Erreur lors de la récupération de l'image")
        except requests.exceptions.RequestException as e:
            print(f"Une erreur s'est produite lors de l'appel API : {e}")
        except Exception as e:
            print("Une erreur est survenue :", e)

