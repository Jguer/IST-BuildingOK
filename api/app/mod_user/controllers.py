import json

from flask import Blueprint, Flask, request, jsonify
from datetime import datetime

from app import db, utils

mod_user = Blueprint("user", __name__, url_prefix="/user")

def get_users_in_range(user_id, range):
    sending_user = db.User.find_one({'ist_ID':user_id})
    list_in_range = db.User.find({'cur_pos': {'$near': {'$geometry': {type: 'Point', coordinates: sending_user['cur_pos']}, '$maxDistance': range}},
    'last_seen': {'$gt': datetime.utcnow() - timedelta(minutes = 10)}})
    return list_in_range

def user_building(user_loc):
    list_cur_buildings = db.Building.find({'location': {'$near': {'$geometry': {type: 'Point', coordinates: user_loc}, '$maxDistance': utils.default_range}}})
    return list_cur_buildings[0].__dict__

def received_messages(user_id):
    user_messages = db.Message.find({'to_istID': user_id})
    return jsonify([obj.__dict___ for obj in user_messages), 200, {
        "ContentType": "application/json"
    }


@mod_user.route(
    "/<user_id>", methods=["GET"])  # receives an authentication token
def register_user(user_id):
    db.User.insert_one({'ist_ID':user_id, 'sentstamp': datetime.now(), 'cur_pos':[0.0,0.0]})
    return ("", 200)


@mod_user.route("/<user_id>/location", methods=["POST"])
def update_loc(user_id):
    content = request.get_json()
    lastseen = db.User.find_one({'ist_ID': user_id})['last_seen']
    db.User.update_one({'ist_ID':user_id},{'$set'z:{'cur_pos':cont['cur_pos']}, '$currentDate':{'last_seen':True}})
    cur_building = user_building(cont['cur_pos'])['building_ID']
    list_last_buildings = db.Activity.find({'ist_ID':user_id, 'departure': lastseen})
    last_building = list_last_buildings[0].__dict__['building_ID']
    if cur_building == last_building:
        db.Activity.update_one({'ist_ID':user_id, 'building_ID': i},{$currentDate:{'departure':True}})
    else:
        db.Activity.insert_one({'ist_ID':user_id, 'building_ID': i, 'arrival': datetime.now(), 'departure': datetime.now()})
    return jsonify({'result': 'True'}), 200


@mod_user.route("/<user_id>/message", methods=["POST", "GET"])
def message_log(user_id):
    if request.method == "POST":
        content = request.get_json()
        from_building = user_building(db.User.find_one({'ist_ID': user_id})['cur_pos'])
        list_nearby_users = [x.__dict__['ist_ID'] for x in get_users_in_range(user_id, cont['radius'])]
        new_messages = [{'from_istID': user_id, 'sentstamp': datetime.utcnow(), 'content': content['content'], 'sent_from': from_building,
        'to_istID': x.__dict__['ist_ID'], 'sent_to': user_building(x.__dict__['cur_pos'])['building_ID']} for x in list_nearby_users]
        result = db.Message.insert_many(new_messages)
        if (len(result.inserted_ids) == len(new_messages)):
            return jsonify({'result': 'True'}), 200
        return jsonify({'result': 'False'}), 200
    return received_messages(user_id)


@mod_user.route("/<user_id>/nearby", methods=["GET"])
def building_users(user_id):
    from_building = user_building(db.User.find_one({'ist_ID': user_id})['cur_pos'])
    in_building = db.User.find({'cur_pos': {'$near': {'$geometry': {type: 'Point', coordinates: from_building['position']}, '$maxDistance': utils.default_range}}})
    return jsonify([obj.__dict___ for obj in in_building), 200, {
        "ContentType": "application/json"
    }


@mod_user.route("/<user_id>/nearby/<range>", methods=["GET"])
def api_nearby_users(user_id, range):
    user_table = get_users_in_range(user_id, range)
    if not user_table:
        return ("", 204)
    return jsonify([obj.__dict___ for obj in user_table), 200, {
        "ContentType": "application/json"
    }
