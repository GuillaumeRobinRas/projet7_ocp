from flask import Flask, request, Blueprint
from handler import feature_importance_handler

analytics = Blueprint('analytics', __name__)


@analytics.route('/loan/bivariate/', methods=['GET'])
def bivariate_analysis():
    pass

@analytics.route('/loan/feature_importance/<int:client_id>', methods=['GET'])
def feature_importance(client_id):
    return feature_importance_handler.FeatureimportanceHandler(client_id).route()


@analytics.route('/loan/distribution/<int:client_id>/<feature_name>', methods=['GET'])
def feature_distribution(client_id, feature_name):
    pass
