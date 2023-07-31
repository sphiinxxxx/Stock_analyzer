import json

from flask import Flask, jsonify
from flask_restful import Api, Resource, abort
from flask_cors import CORS
from Model.ann_model import find
import tensorflow as tf
from tensorflow import keras
import yfinance as yf

app = Flask(__name__)
cors = CORS(app)
api = Api(app)

app.config['CORS_HEADERS'] = 'Content-Type'

list_stocks = ['SPY', 'TSLA', 'FB', 'GOOG', 'GOOGL', 'AAPL', 'TTM', 'RELI']


class Stock_ANN(Resource):
    def get(self, stock_name):
        try:
            if stock_name not in list_stocks:
                print("Invalid stock name")
            else:
                model = keras.models.load_model(
                    "Models/ANN/{}.h5".format(stock_name))
                #prediction = model.predict(X_test)

                data = yf.download(stock_name, auto_adjust=True)
                #score = model.evaluate(X_train, Y_train, verbose = 0)
                #print("Accuracy = ", (100-score), "%")

                data = data.iloc[len(data)-10:]
                data = data[['High', 'Open', 'Volume']]
                pred = model.predict(data, verbose=0)
                res = {'p1': {'today_closing_price': pred[0][0]}}

                # res = find(stock_name)
                # if res[0] == -1 or

                # print(res)
                res = json.dumps(str(res))
                response = jsonify({'data': res})
                response.headers.add("Access-Control-Allow-Origin", "*")
                return response
        except Exception as e:
            print("SERVER ERROR 500")
            print(e)


api.add_resource(Stock_ANN, '/stock_ann/<string:stock_name>')
