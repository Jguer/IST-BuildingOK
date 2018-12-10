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
    last_seen = db.Column(db.DateTime)
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
    sentstamp = db.Column(db.DateTime, primary_key = True) #timestamp given by server
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

@app.route('/user/<id>', methods=['POST']) #receives an authentication token
#login function
#if the user is not on the database, add him to it
pass

@app.route('/user/<id>/location', methods=['POST'])
def update_loc(id):
    content = request.get_json()
    update_coord(content, id)
    return json.dumps({'success':True}),200,{'ContentType':'application/json'}

@app.route('/user/<id>/message', methods=['POST', 'GET'])
def message_log(id):
    if request.method == 'POST':
        content = request.get_json()
        post_message(content, id)
        return json.dumps({'success':True}),200,{'ContentType':'application/json'}
    return sent_messages()

@app.route('/user/<id>/nearby/<range>', methods=['GET'])
def update_loc(id):
    user_table = get_users_in_range(id, range)
    if not user_table:
        return ('',204)
    return json.dumps(jsonify(user_table)),200,{'ContentType':'application/json'}

@app.route('/admin/users', methods=['GET'])
def check_online_users():
    online_table = get_users_online()
    if not online_table:
        return ('',204)
    return json.dumps(jsonify(online_table)),200,{'ContentType':'application/json'}

@app.route('/building', methods=['GET','POST'])
def buildings():
    if request.method == 'GET':
        return json.dumps(jsonify(buildings_table)),200,{'ContentType':'application/json'}
    content = request.get_json()
    insert_building(content)
    return json.dumps({'success':True}),200,{'ContentType':'application/json'}

@app.route('/admin/users/<build_id>', methods=['GET'])
def users_inside(build_id):
    inside_table = get_users_online()
    if not inside_table:
        return ('',204)
    return json.dumps(jsonify(inside_table)),200,{'ContentType':'application/json'}

@app.route('/user', methods=['GET'])
def show_users():
    online_table = get_users_online()
    if not online_table:
        return ('',204)
    return json.dumps(jsonify(online_table)),200,{'ContentType':'application/json'}

@app.route('/log/user/<usr_id>', methods=['GET'])
def user_log(usr_id):
    all_usr_actions = get_users_online()
    if not all_usr_actions:
        return ('',204)
    return json.dumps(jsonify(all_usr_actions)),200,{'ContentType':'application/json'}

@app.route('/log/building/<build_id>', methods=['GET'])
def build_log(build_id):
    all_build_actions = get_users_online()
    if not all_build_actions:
        return ('',204)
    return json.dumps(jsonify(all_build_actions)),200,{'ContentType':'application/json'}

if __name__ == '__main__':
    app.run()
