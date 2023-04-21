from datetime import datetime
from turtle import pd
from flask import Flask, jsonify, request, render_template
from pymongo import MongoClient
from bson import ObjectId
import json


class CustomJSONEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, ObjectId):
            return str(obj)
        return json.JSONEncoder.default(self, obj)

app = Flask(__name__)

app.json_encoder = CustomJSONEncoder

MONGO_URI = "mongodb://robgoudis:Password123@ac-9wgptts-shard-00-00.81vbxyz.mongodb.net:27017,ac-9wgptts-shard-00-01.81vbxyz.mongodb.net:27017,ac-9wgptts-shard-00-02.81vbxyz.mongodb.net:27017/?ssl=true&replicaSet=atlas-z80eec-shard-0&authSource=admin&retryWrites=true&w=majority"
client = MongoClient(MONGO_URI)
db=client.get_database("stocks_db")
records = db.intraday


# Homepage
@app.route('/')
def index():
    return render_template('index.html') 


# Line-chart page
@app.route('/google-charts/line-chart')
def google_line_chart():
        stockdata =list(records.find())
        #print(data)
        return render_template('line-chart.html', stockdata=stockdata)



# For Bonus 1- API Get all items
@app.route("/stocks")
def get_all_stocks():
    stocks = list(records.find())
    return jsonify(stocks)


# For Bonus 2- API Get a range of items
@app.route("/stocks/<start_time>/<end_time>")
def get_stocks_by_date_range(start_time, end_time):
    query = {
    "Time Series (5min)": {
        "$gte": {
            start_time: {
                "$exists": True
            }
        },
        "$lte": {
            end_time: {
                "$exists": True
            }
        }
    }
    }
    stocks = list(records.find(query, {"_id": 0}))
    return jsonify(stocks)


# For Bonus 3- API Get item by ID
@app.route("/stocks/<id>")
def get_stock_by_id(id):
    stock = records.find_one({'_id': ObjectId(id)})
    return jsonify(stock)



if __name__ == "__main__":
   app.run()