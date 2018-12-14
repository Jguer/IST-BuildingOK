import json

from flask import Blueprint, jsonify, request
from app import db
import datetime

mod_admin = Blueprint("admin", __name__, url_prefix="/admin")



@mod_admin.route("/online", methods=["GET"])
def check_online_users():
    compare = datetime.datetime.utcnow() - datetime.timedelta(minutes=10)
    online = db.User.find({'last_seen': {'$gt': compare})
    if not online:
        return ("", 204)
    return jsonify([ob.__dict__ for ob in online]), 200, {
        "ContentType": "application/json"
    }


@mod_admin.route("/building", methods=["GET", "POST"])
def buildings():
    if request.method == "GET":
        all_buildings_table = db.Building.find({})
        if not all_buildings_table:
            return ("", 204)
        return jsonify([ob.__dict__ for ob in all_buildings_table]), 200, {
            "ContentType": "application/json"
    elif request.method == "POST":
        content = request.json
        to_add = [{'building_ID' : i['id'], 'name': i['name'], 'position': i['position']} for i in content]
        result = db.Building.insert_many(to_add)
        if (len(result.inserted_ids) == len(to_add)):
            return jsonify({'result': 'True'}), 200
        return jsonify({'result': 'False'}), 200


@mod_admin.route("/users/<build_id>", methods=["GET"])
def users_inside(build_id):
    compare = datetime.datetime.utcnow() - datetime.timedelta(minutes=10)
    build_pos = db.Building.find_one({'id': build_id})['position']
    online_table = db.User.find({'last_seen': {'$gt': compare}, cur_pos: {'$near': {'$geometry': {type: 'Point', coordinates: build_pos},
     '$maxDistance': utils.default_range}}})
    if not online_table:
        return ("", 204)
    return jsonify([ob.__dict__ for ob in online_table]), 200, {
        "ContentType": "application/json"
    }


@mod_admin.route("/users", methods=["GET"])
def show_users():
    all_users_table = db.User.find({})
    return jsonify([ob.__dict__ for ob in all_users_table])


@mod_admin.route("/log/user/<usr_id>", methods=["GET"])
def user_log(usr_id):
    user_actions = db.Activity.find({'ist_ID': usr_id})
    user_actions += db.Message.find({'$or': ['from_istID': usr_id, 'to_istID': usr_id]})
    if not user_actions:
        return ("", 204)
    return (
        jsonify([ob.__dict__ for ob in user_actions]),
        200,
        {
            "ContentType": "application/json"
        },
    )


@mod_admin.route("/log/building/<build_id>", methods=["GET"])
def build_log(build_id):
    build_actions = db.Activity.find({'building_ID': usr_id})
    build_actions += db.Message.find({'$or': ['sent_from': usr_id, 'sent_to': usr_id]})
    if not build_actions:
        return ("", 204)
    return (
        jsonify([ob.__dict__ for ob in build_actions]),
        200,
        {
            "ContentType": "application/json"
        },
    )
