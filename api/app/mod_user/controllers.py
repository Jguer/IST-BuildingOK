import json

from flask import Blueprint, Flask, jsonify, request
from sqlalchemy import update
import datetime, math

from app import db, utils
import app.models as models

mod_user = Blueprint("user", __name__, url_prefix="/user")

def update_coord(cont, user_id):
    updt_user = db.session.query(User).filter_by(ist_ID = user_id)
    updt_user.cur_pos_lat = cont['lat']
    updt_user.cur_pos_long = cont['long']
    list_buildings = db.session.query(Building).filter(utils.dist(updt_user.cur_pos_lat, Building.cur_pos_lat, updt_user.cur_pos_long, Building.cur_pos_long) < utils.default_range)
    return

def post_message(cont, user_id):
    new_msg = models.UserMessage(from_istID = user_id, sentstamp = datetime.datetime.now(), radius = cont['radius'], content = cont['content'])
    db.session.add(new_msg)
    db.session.flush()
    return

def get_users_in_range(user_id, range):
    sending_user = db.session.query(User).filter_by(ist_ID = user_id)
    list_in_range = db.session.query(User).filter(utils.dist(User.cur_pos_lat, sending_user.cur_pos_lat, User.cur_pos_long, sending_user.cur_pos_long) < range)
    return list_in_range

@mod_user.route(
    "/<user_id>", methods=["GET"])  # receives an authentication token
def register_user(user_id):
    u = models.User(
        ist_ID=user_id, cur_pos_lat=0, cur_pos_long=0)
    print("user created", u)
    db.session.add(u)
    db.session.commit()
    return ("", 200)

@mod_user.route("/<user_id>/location", methods=["POST"])
def update_loc(user_id):
    content = request.get_json()
    update_coord(content, user_id)
    return json.dumps({
        "success": True
    }), 200, {
        "ContentType": "application/json"
    }


@mod_user.route("/<user_id>/message", methods=["POST", "GET"])
def message_log(user_id):
    if request.method == "POST":
        content = request.get_json()
        post_message(content, user_id)
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
