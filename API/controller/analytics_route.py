from flask import Flask, request, Blueprint


@analytics.route('/loan/bivariate/', methods=['GET'])
def bivariate_analysis():
    pass


@analytics.route('/loan/feature_importance/<int:client_id>', methods=['GET'])
def feature_importance(client_id):
    pass


@analytics.route('/loan/distribution/<int:client_id>/<feature_name>', methods=['GET'])
def feature_distribution(client_id, feature_name):
    pass
