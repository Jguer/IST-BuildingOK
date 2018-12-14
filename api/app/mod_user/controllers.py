import json

from flask import Blueprint, Flask, request
from datetime import datetime

from app import db, utils

mod_user = Blueprint("user", __name__, url_prefix="/user")

def get_users_in_range(user_id, range):
    sending_user = db.User.find_one({'ist_ID':user_id})
    list_in_range = db.User.find({'cur_pos': {$near: {$geometry: {type: 'Point', coordinates: sending_user['cur_pos']}, $maxDistance: range}}})
    return list_in_range

@mod_user.route(
    "/<user_id>", methods=["GET"])  # receives an authentication token
def register_user(user_id):
    db.User.insert_one({'ist_ID':user_id, 'sentstamp': datetime.now(), 'cur_pos':[0.0,0.0]})
    return ("", 200)

@mod_user.route("/<user_id>/location", methods=["POST"])
def update_loc(user_id):
    content = request.get_json()
    lastseen = db.User.find_one({'ist_ID': user_id})['last_seen']
    db.User.update_one({'ist_ID':user_id},{$set{'cur_pos':cont['cur_pos']}, $currentDate:{'last_seen':True}})
    list_cur_buildings = db.Building.find({'location': {$near: {$geometry: {type: 'Point', coordinates: cont['cur_pos']}, $maxDistance: range}}})
    list_cur_buildings = [x.__dict__['building_ID'] for x in list_cur_buildings]
    list_last_buildings = db.Activity.find({'ist_ID':user_id, 'departure': lastseen})
    list_last_buildings = [x.__dict__['building_ID'] for x in list_last_buildings]
    for i in list_cur_buildings:
        if i in list_last_buildings:
            db.Activity.update_one({'ist_ID':user_id, 'building_ID': i},{$currentDate:{'departure':True}})
        else:
            db.Activity.insert_one({'ist_ID':user_id, 'building_ID': i, 'arrival': datetime.now(), 'departure': datetime.now()})
    return json.dumps({
        "success": True
    }), 200, {
        "ContentType": "application/json"
    }


@mod_user.route("/<user_id>/message", methods=["POST", "GET"])
def message_log(user_id):
    if request.method == "POST":
        content = request.get_json()
        list_nearby_users = [x.__dict__['ist_ID'] for x in get_users_in_range(user_id, cont['radius'])]
        new_messages = [{'from_istID': user_id, 'sentstamp': datetime.utcnow(), 'content': content['content']}]
        db.UserMessage.insert_one({'from_istID': user_id, 'sentstamp': datetime.utcnow(), 'radius': cont['radius'], 'content': cont['content']})
        return json.dumps({
            "success": True
        }), 200, {
            "ContentType": "application/json"
        }
    return sent_messages()


@mod_user.route("/<user_id>/nearby/<range>", methods=["GET"])
def api_nearby_users(user_id, range):
    user_table = get_users_in_range(user_id, range)
    if not user_table:
        return ("", 204)
    return json.dumps(jsonify([obj.__dict___ for obj in user_table)), 200, {
        "ContentType": "application/json"
    }
