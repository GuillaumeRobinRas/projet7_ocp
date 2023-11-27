from flask import Flask, request, Blueprint
from Handler import feature_importance_handler, bivariate_analysis_handler, feature_distribution_handler

analytics = Blueprint('analytics', __name__)


@analytics.route('/loan/bivariate/', methods=['GET'])
def bivariate_analysis():
    return bivariate_analysis_handler.BivariateAnalysisHandler().route()


@analytics.route('/loan/feature_importance/<int:client_id>', methods=['GET'])
def feature_importance(client_id):
    return feature_importance_handler.FeatureimportanceHandler(client_id).route()


@analytics.route('/loan/distribution/<int:client_id>/<feature_name>', methods=['GET'])
def feature_distribution(client_id, feature_name):
    return feature_distribution_handler.FeatureDistributionHandler(client_id, feature_name).route()
