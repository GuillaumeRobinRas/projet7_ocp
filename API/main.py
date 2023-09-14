from flask import Flask
from env import lgb_model_path
from projet7_ocp.API.utils.utils import load_model
import pandas as pd
from route import prediction_route, analytics_route

app = Flask(__name__)
model_lgb = load_model(lgb_model_path)
df = pd.read_csv('../dataset.csv')


if __name__ == '__main__':
    app.register_blueprint(prediction_route.prediction)
    app.register_blueprint(analytics_route.analytics)
    app.run(debug=True)
