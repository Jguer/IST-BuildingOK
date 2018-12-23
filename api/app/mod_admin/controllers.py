from datetime import datetime, timedelta
import hashlib
from bson.json_util import dumps

from flask import Blueprint, jsonify, request
from app import db
import app.utils as utils

mod_admin = Blueprint("admin", __name__, url_prefix="/admin")


@mod_admin.route("/online", methods=["GET"])
def check_online_users():
    compare = datetime.utcnow() - timedelta(minutes=10)
    online = db.User.find({'last_seen': {'$gt': compare}})
    if not online:
        return ("", 204)
    return (
        dumps(online),
        200,
        {
            "ContentType": "application/json"
        },
    )


@mod_admin.route("/building", methods=["GET", "POST"])
def buildings():
    if (request.method == "GET"):
        all_buildings_table = db.Building.find({})
        if not all_buildings_table:
            return ("", 204)
        return (
            dumps(all_buildings_table),
            200,
            {
                "ContentType": "application/json"
            },
        )
    elif (request.method == "POST"):
        content = request.json
        to_add = [{
            '_id': hashlib.sha1(i['name'].encode()).hexdigest(),
            'name': i['name'],
            'position': [float(x) for x in i['position']]
        } for i in content]
        result = db.Building.insert_many(to_add)
        if (len(result.inserted_ids) == len(to_add)):
            return jsonify({'result': 'True'}), 200
        return jsonify({'result': 'False'}), 200


@mod_admin.route("/users/<build_id>", methods=["GET"])
def users_inside(build_id):
    compare = datetime.utcnow() - timedelta(minutes=10)
    build_pos = db.Building.find_one({'_id': build_id})['position']
    online_table = db.User.find({
        'last_seen': {
            '$gt': compare
        },
        'cur_pos': {
            '$near': {
                '$geometry': {
                    'type': 'Point',
                    'coordinates': build_pos
                },
                '$maxDistance': utils.default_range
            }
        }
    })
    if not online_table:
        return ("", 204)
    return (
        dumps(online_table),
        200,
        {
            "ContentType": "application/json"
        },
    )


@mod_admin.route("/users", methods=["GET"])
def show_users():
    all_users_table = db.User.find({})
    return (
        dumps(all_users_table),
        200,
        {
            "ContentType": "application/json"
        },
    )


@mod_admin.route("/log/user/<usr_id>", methods=["GET"])
def user_log(usr_id):
    user_actions = list(db.Activity.find({'ist_ID': usr_id}))
    user_actions += list(db.Message.find({
        '$or': [{
            'from_istID': usr_id
        }, {
            'to_istID': usr_id
        }]
    }))
    if not user_actions:
        return ("", 204)
    return (
        dumps(user_actions),
        200,
        {
            "ContentType": "application/json"
        },
    )


@mod_admin.route("/log/building/<build_id>", methods=["GET"])
def build_log(build_id):
    build_actions = list(db.Activity.find({'building_ID': build_id}))
    build_actions += list(db.Message.find({
        '$or': [{
            'sent_from': build_id
        }, {
            'sent_to': build_id
        }]
    }))
    if not build_actions:
        return ("", 204)
    return (
        dumps(build_actions),
        200,
        {
            "ContentType": "application/json"
        },
    )
