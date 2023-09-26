from flask import Flask, jsonify, request
from env import lgb_model_path
import json
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import io
import numpy as np
from PIL import Image

from handler.abstract_client_handler import AbstractClientHandler


class FeatureDistributionHandler(AbstractClientHandler):

    def __init__(self, client_id: int, feature: str):
        super().__init__(client_id)
        self.feature = feature

    def make_graph(self, client_feature_value):
        plt.figure(figsize=(10, 6))
        sns.histplot(data=self.df, x=self.feature, hue='TARGET', multiple='stack', kde=True)
        plt.title(f'Distribution de la fonctionnalité {self.feature} en fonction de la classe')
        plt.axvline(x=client_feature_value, color='red', linestyle='dashed', label='Client')
        plt.legend()
        buffer = io.BytesIO()
        plt.savefig(buffer, format='png')
        buffer.seek(0)
        return buffer

    def route(self):
        try:
            if self.is_a_client() and self.is_a_feature(self.feature):
                buffer = self.make_graph(self.get_client()[self.feature].values[0])
                img = self.convert_to_base64(buffer)
                return jsonify({"image": img})
            else:
                return jsonify({"error": "Client or feature not found"}), 404
        except Exception as e:
            print(e)
            return jsonify({"error": "An error occurred"}), 500
