import streamlit as st
from ENV import LOGO_PATH, INITIAL_SENTENCE
from PIL import Image
from io import BytesIO
import base64
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


class LoanPredictorUI:
    def __init__(self, df):
        self.df = df

    @staticmethod
    def header() -> None:
        #logo = LoanPredictorUI.read_image(LOGO_PATH)
        #st.image(logo, use_column_width=True)
        st.title('Estimation de risque de défaut de paiement de prêt immobilier')

    def sidebar(self) -> list:
        st.sidebar.header('Choix du client :')
        customer_id = st.sidebar.text_input(INITIAL_SENTENCE)
        st.subheader('Paramètres du prêt')
        loan_amount = st.sidebar.number_input("Montant du prêt", value=0)
        age = st.sidebar.number_input("Âge du client", value=0)
        income = st.sidebar.number_input("Revenus du client", value=0)
        loan_duration_months = st.sidebar.number_input("Durée du prêt (mois)", value=0)
        gender = st.sidebar.number_input("genre", value=0)
        feature1 = st.sidebar.selectbox("Sélectionner la première fonctionnalité", self.df.columns)
        feature2 = st.sidebar.selectbox("Sélectionner la deuxième fonctionnalité", self.df.columns)
        distributeed_feature = st.sidebar.selectbox("Sélectionner une features pour voir la distribution", self.df.columns)
        if st.sidebar.button('calculer ce prêt'):
            return [customer_id, loan_amount, age, income, loan_duration_months, gender, feature1, feature2, distributeed_feature]
        return [customer_id, feature1, feature2, distributeed_feature]

    @staticmethod
    def display_top_client_features(top_features: list, top_n=5) -> None:
        st.subheader(f"Top {top_n} des fonctionnalités importantes pour le client :")
        top_features_df = pd.DataFrame(top_features[:top_n])
        plt.figure(figsize=(10, 6))
        sns.barplot(x='importance', y='column_name', data=top_features_df, orient='h')
        plt.xlabel('Importance')
        plt.ylabel('Fonctionnalités')
        plt.title(f'Top {top_n} des fonctionnalités importantes')
        st.pyplot(plt)


    @staticmethod
    def display_risk(risk: bool) -> None:
        if risk:
            st.error("Le client est considéré comme risqué")
        else:
            st.success("Le client n'est pas considéré comme risqué")

    @staticmethod
    def display_client_probabilities(probabilities: list):
        ok = round(probabilities[0][0], 3)*100
        notok = round(probabilities[0][1], 3)*100
        st.subheader('Probabilités du client')
        if ok < 0.5:
            st.write(f'La probabilité de défaut de paiement du client est de {notok}%')
        else:
            st.write(f'La probabilité de recouvrement du client est de {ok}%')

    def display_client_risk_and_probabilities(self, risk: bool, probabilities: list) -> None:
        self.display_risk(risk)
        self.display_client_probabilities(probabilities)


    @staticmethod
    @st.cache_data
    def read_image(path: str) -> Image:
        return Image.open(path)

    @staticmethod
    def display_bivariate_analysis(image_base64: str) -> None:
        image = Image.open(BytesIO(base64.b64decode(image_base64)))
        st.subheader("Analyse bivariée")
        st.image(image, use_column_width=True)

    @staticmethod
    def display_feature_distribution(feature_name: str, image: Image) -> None:
        st.subheader(f"Distribution de la fonctionnalité '{feature_name}' en fonction de la classe :")
        st.image(image, use_column_width=True)



