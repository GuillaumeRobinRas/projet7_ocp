import streamlit as st
import pandas as pd
import base64
import io

from ENV import DF_PATH


class LoanPredictorController:

    def __init__(self):
        self.customer_data = []
        self.client_list = []

    def set_customer_data(self, customer_data):
        self.customer_data = customer_data

    def get_customer_data(self):
        return self.customer_data

    def set_client_list(self, client_list):
        self.client_list = client_list

    @staticmethod
    def is_risky(prediction):
        if prediction == 1:
            return True
        else:
            return False

    def client_is_valid(self):
        try:
            if int(self.customer_data[0]) in self.client_list:
                return True
            else:
                return False
        except ValueError:
            return False

    def isvalid(self):
        try:
            data_dict = self.data_mapper()
        except ValueError:
            return False
        if len(self.customer_data) > 1:
            if data_dict["customer_id"] not in self.client_list:
                return False
            if data_dict["loan_amount"] < 0:
                return False
            if data_dict["age"] < 0:
                return False
            if data_dict["income"] < 0:
                return False
            if data_dict["loan_duration_months"] < 0:
                return False
        else:
            return False
        return True

    def data_mapper(self):
        print("valid")
        mapper = {
            "customer_id": float(self.customer_data[0]),
            "loan_amount": float(self.customer_data[1]),
            "age": int(self.customer_data[2]),
            "income": float(self.customer_data[3]),
            "loan_duration_months": int(self.customer_data[4]),
            "gender": self.customer_data[5],
            "feature1": self.customer_data[6],
            "feature2": self.customer_data[7],
            "distribution_feature": self.customer_data[8]
        }
        return mapper

    def tiny_mapper(self):
        return {
            "customer_id": float(self.customer_data[0]),
            "feature1": self.customer_data[1],
            "feature2": self.customer_data[2],
            "distribution_feature": self.customer_data[3]
        }
