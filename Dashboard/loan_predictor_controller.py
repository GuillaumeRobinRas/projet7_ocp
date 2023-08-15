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
            customer_id, loan_amount, age, income, loan_duration_months, gender = self.customer_data
        except ValueError:
            return False
        if len(self.customer_data) > 1:
            if int(customer_id) not in self.client_list:
                return False
            if loan_amount < 0:
                return False
            if age < 0:
                return False
            if income < 0:
                return False
            if loan_duration_months < 0:
                return False
        else:
            return False
        return True


