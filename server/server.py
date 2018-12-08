from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)
db = SQLAlchemy(app)

class User(db.Model):
    # Columns
    ist_ID = db.Column(db.String(9), primary_key = True)
    cur_pos_lat = db.Column(db.Float)
    cur_pos_long = db.Column(db.Float)
    #inBuilding query: SELECT buildingID from Building B, User U where sqrt((U.cur_pos_lat - B.location_lat)^2 + (U.cur_pos_lat - B.location_lat)^2) < radius

class Building(db.Model):
    building_ID = db.Column(db.BigInteger, primary_key = True)
    location_lat = db.Column(db.Float)
    location_long = db.Column(db.Float)
    name = db.Column(db.String(128))

class Stay(db.Model):
    ist_ID = db.Column(db.String(9), primary_key = True)
    arrival = db.Column(db.DateTime, primary_key = True)
    departure = db.Column(db.DateTime)
    buildingID = db.Column(db.BigInteger)

class UserMessage(db.Model):
    from_istID = db.Column(db.String(9), primary_key = True)
    sentstamp = db.Column(db.DateTime, primary_key = True)
    radius = db.Column(db.Float)
    content = db.Column(db.Text)

class BotMessage(db.Model):
    to_buildingID = db.Column(db.BigInteger, primary_key = True)
    sentstamp = db.Column(db.DateTime, primary_key = True)
    content = db.Column(db.Text)
    bot_ID = db.Column(db.Integer, primary_key = True)

@app.route('/')
def hello_world():
    return 'Hello World!'

@app.route('/json2')
def ret_jsonjson():
    return jsonify({"aaa": 12, "bbb": ["bbb", 12, 12]})


if __name__ == '__main__':
    app.run()
