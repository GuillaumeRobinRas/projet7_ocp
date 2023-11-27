from flask import jsonify

from .abstract_client_handler import AbstractClientHandler


class FeatureimportanceHandler(AbstractClientHandler):

    def __init__(self, client_id: int):
        super().__init__(client_id)

    def get_feature_importance(self):
        feature_importance = self.model_lgb.feature_importances_
        return feature_importance.tolist()

    @property
    def booster_model(self):
        booster = self.model_lgb.booster_
        return booster

    @staticmethod
    def sort_client_feature_importance(client_importance: dict):
        return sorted(client_importance.values(), key=lambda item: item["importance"],
                      reverse=True)

    def get_client_feature_importance_gain(self):
        return self.booster_model.feature_importance(importance_type='gain') * self.get_client().values[0]

    def get_client_feature_importance_split(self):
        return self.booster_model.feature_importance(importance_type='split') * self.get_client().values[0]

    def get_client_feature_importance_weight(self):
        return self.booster_model.feature_importance(importance_type='weight') * self.get_client().values[0]

    def make_client_importance_dict(self, client_importance):
        client_importance_dict = {}
        for i, importance_value in enumerate(client_importance):
            column_name = self.df.columns[i]
            client_importance_dict[column_name] = {
                "importance": importance_value,
                "column_name": column_name
            }
        return client_importance_dict

    def route(self):
        if self.is_a_client():
            client_importance_dict = self.make_client_importance_dict(self.get_client_feature_importance_split())
            return jsonify(self.sort_client_feature_importance(client_importance_dict)), 200
        else:
            return jsonify({"error": "Client not found"}), 404

