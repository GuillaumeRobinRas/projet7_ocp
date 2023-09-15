from flask import Flask
import pandas as pd

from controller import prediction_route

app = Flask(__name__)
app.register_blueprint(prediction_route.prediction)

if __name__ == '__main__':
    app.run(debug=True)
