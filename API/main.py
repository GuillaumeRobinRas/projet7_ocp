from flask import Flask, jsonify, request
from env import lgb_model_path
from utils import load_model
import json
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import io
import base64
import numpy as np
from PIL import Image
from route import prediction_route, analytics_route

app = Flask(__name__)
model_lgb = load_model(lgb_model_path)
df = pd.read_csv('../dataset.csv')


if __name__ == '__main__':
    app.register_blueprint(prediction_route.prediction)
    app.register_blueprint(analytics_route.analytics)
    app.run(debug=True)


