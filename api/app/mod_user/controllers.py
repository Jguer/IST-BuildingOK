import json

from flask import Blueprint, Flask, request
from datetime import datetime

from app import db, utils

mod_user = Blueprint("user", __name__, url_prefix="/user")

def get_users_in_range(user_id, range):
    sending_user = db.User.find_one({'ist_ID':user_id})
    list_in_range = db.User.find({cur_pos: {$near: {$geometry: {type: 'Point', coordinates: sending_user['cur_pos']}, $maxDistance: range}}})
    return list_in_range

@mod_user.route(
    "/<user_id>", methods=["GET"])  # receives an authentication token
def register_user(user_id):
    db.User.insert_one({'ist_ID':user_id, 'sentstamp': datetime.now(), 'cur_pos':[0.0,0.0]})
    return ("", 200)

@mod_user.route("/<user_id>/location", methods=["POST"])
def update_loc(user_id):
    content = request.get_json()
    db.User.update_one({'ist_ID':user_id},{$set{'cur_pos':cont['cur_pos']}, $currentDate:{'last_seen':True}})
    return json.dumps({
        "success": True
    }), 200, {
        "ContentType": "application/json"
    }


@mod_user.route("/<user_id>/message", methods=["POST", "GET"])
def message_log(user_id):
    if request.method == "POST":
        content = request.get_json()
        db.UserMessage.insert_one({'from_istID': user_id, 'sentstamp': datetime.utcnow(), 'radius' = cont['radius'], 'content': cont['content']})
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
    return json.dumps(jsonify(user_table)), 200, {
        "ContentType": "application/json"
    }
