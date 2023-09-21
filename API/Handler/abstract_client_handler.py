from abc import ABC, abstractmethod
import pandas as pd


from env import lgb_model_path, df_path
from utils.utils import load_model
from utils.utils import load_model


class AbstractClientHandler(ABC):
    def __init__(self, client_id: int):
        self.df = pd.read_csv(df_path)
        self.model_lgb = load_model(lgb_model_path)
        self.client_id = client_id

    @abstractmethod
    def route(self):
        raise NotImplementedError("Subclasses must implement the 'execute' method.")

    def is_a_client(self) -> bool:
        return self.client_id in self.df['SK_ID_CURR'].tolist()

    def get_client(self) -> pd.DataFrame:
        client = self.df[self.df['SK_ID_CURR'] == int(self.client_id)]
        print(client.shape)
        client = client.iloc[:, 1:750]  # ligne à check car c'est un hotfix bizarre
        return client

    def get_prediction(self, client: pd.DataFrame) -> list:
        prediction = self.model_lgb.predict(client)
        return prediction.tolist()

    def get_probabilities(self, client: pd.DataFrame) -> list:
        probabilities = self.model_lgb.predict_proba(client)
        return probabilities.tolist()
