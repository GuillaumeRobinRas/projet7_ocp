import streamlit as st
import pandas as pd
from loan_predictor_ui import LoanPredictorUI
from API_requester import APIRequester
from loan_predictor_controller import LoanPredictorController
from ENV import DF_PATH
import base64
import io

st.set_page_config(page_title="Prédictions de risque de prêt")


class LoanPredictorApp:
    def __init__(self):
        self.df = self.get_df()
        self.api_requester = APIRequester()
        self.ui = LoanPredictorUI(self.df)
        self.controller = LoanPredictorController()

    def get_df(self):
        df = self.read_csv(DF_PATH)
        return df

    @property
    def list_of_client_id(self):
        return list(self.df['SK_ID_CURR'])

    @staticmethod
    @st.cache_data
    def read_csv(path: str) -> pd.DataFrame:
        return pd.read_csv(path)

    def run(self):

        predictions = False
        feature1 = ""
        feature2 = ""
        distribution_feature = ""
        customer_id = 0
        self.controller.set_client_list(self.list_of_client_id)
        self.ui.header()
        customer_data = self.ui.sidebar()
        self.controller.set_customer_data(customer_data)
        if self.controller.client_is_valid():
            customer_id = int(customer_data[0])
            feature1 = customer_data[1]
            feature2 = customer_data[2]
            distribution_feature = customer_data[3]
            if self.controller.isvalid():
                loan_amount = float(customer_data[1])
                age = int(customer_data[2])
                income = float(customer_data[3])
                loan_duration_months = int(customer_data[4])
                gender = customer_data[5]
                feature1 = customer_data[6]
                feature2 = customer_data[7]
                distribution_feature = customer_data[8]
                predictions = self.api_requester.loan_probabilities_custom_client(customer_id,
                                                                                  loan_amount,
                                                                                  age,
                                                                                  income,
                                                                                  loan_duration_months,
                                                                                  gender)

            else:
                predictions = self.api_requester.loan_probabilities_call(customer_id)

        if predictions:
            self.ui.display_client_risk_and_probabilities(risk=self.controller.is_risky(predictions["prediction"]),
                                                          probabilities=predictions["probabilities"])
            self.ui.display_top_client_features(self.api_requester.client_features_importance_call(customer_id))
            self.ui.display_feature_distribution(distribution_feature, self.api_requester.feature_distribution(customer_id, distribution_feature))
            bivariate_data = self.api_requester.bivariate_analysis(customer_id, feature1, feature2)
            if bivariate_data and "image" in bivariate_data:
                self.ui.display_bivariate_analysis(bivariate_data["image"])
        else:
            st.write("Veuillez saisir un numéro de client pour effectuer une prédiction")


if __name__ == "__main__":
    app = LoanPredictorApp()
    app.run()
