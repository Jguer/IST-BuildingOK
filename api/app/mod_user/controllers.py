from flask import Blueprint, request, jsonify
from datetime import datetime, timedelta
from bson.json_util import dumps

from app import db, utils

mod_user = Blueprint("user", __name__, url_prefix="/user")


def get_users_in_range(user_id, radius):
    sending_user = db.User.find_one({'_id': user_id})
    in_range = db.User.find({
        'cur_pos': {
            '$near': {
                '$geometry': {
                    'type': 'Point',
                    'coordinates': sending_user['cur_pos']
                },
                '$maxDistance': radius
            }
        },
        'last_seen': {
            '$gt': datetime.utcnow() - timedelta(minutes=10)
        }
    })
    return [x for x in list(in_range) if x['_id'] != user_id]


def user_building(user_loc):
    list_cur_buildings = list(
        db.Building.find({
            'position': {
                '$near': {
                    '$geometry': {
                        'type': 'Point',
                        "coordinates": user_loc
                    },
                    '$maxDistance': utils.default_range
                }
            }
        }))
    if not list_cur_buildings:
        return None
    return list_cur_buildings[0]


def received_messages(user_id):
    user_messages = db.Message.find({'to_istID': user_id})
    return (
        dumps(user_messages),
        200,
        {
            "ContentType": "application/json"
        },
    )


@mod_user.route(
    "/<user_id>", methods=["GET"])  # receives an authentication token
def register_user(user_id):
    if db.User.find_one({'_id': user_id}) is None:
        db.User.insert_one({
            '_id': user_id,
            'last_seen': datetime.now(),
            'cur_pos': [0.0, 0.0]
        })
    return ("", 200)


@mod_user.route("/<user_id>/location", methods=["POST"])
def update_loc(user_id):
    cont = request.get_json()
    cur_pos = [float(i) for i in cont['cur_pos']]
    lastseen = db.User.find_one({'_id': user_id})['last_seen']
    db.User.update_one({
        '_id': user_id
    }, {
        '$set': {
            'cur_pos': cur_pos
        },
        '$currentDate': {
            'last_seen': True
        }
    })
    cur_building = user_building(cur_pos)
    list_last_buildings = [
        ob.__dict__ for ob in db.Activity.find({
            'ist_ID': user_id,
            'departure': lastseen
        })
    ]
    if list_last_buildings:
        if cur_building == list_last_buildings[0]['building_ID']:
            db.Activity.update_one({
                'ist_ID': user_id,
                'building_ID': cur_building
            }, {'$currentDate': {
                'departure': True
            }})
        elif cur_building:
            db.Activity.insert_one({
                'ist_ID': user_id,
                'building_ID': cur_building['_id'],
                'arrival': datetime.now(),
                'departure': datetime.now()
            })
    else:
        if cur_building:
            db.Activity.insert_one({
                'ist_ID': user_id,
                'building_ID': cur_building['_id'],
                'arrival': datetime.now(),
                'departure': datetime.now()
            })
    return jsonify({'result': 'True'}), 200


@mod_user.route("/<user_id>/message", methods=["POST", "GET"])
def message_log(user_id):
    if request.method == "POST":
        cont = request.get_json()
        from_building = user_building(
            db.User.find_one({
                '_id': user_id
            })['cur_pos'])
        list_nearby_users = get_users_in_range(user_id, float(cont['radius']))
        if list_nearby_users:
            new_messages = [{
                'from_istID': user_id,
                'sentstamp': datetime.utcnow(),
                'content': cont['content'],
                'sent_from': from_building,
                'to_istID': x['_id'],
                'sent_to': user_building(x['cur_pos'])['_id']
            } for x in list_nearby_users]
            result = db.Message.insert_many(new_messages)
            if (len(result.inserted_ids) == len(new_messages)):
                return jsonify({'result': 'True'}), 200
            return jsonify({'result': 'False'}), 200
        else:
            return ("", 204)
    return received_messages(user_id)


@mod_user.route("/<user_id>/nearby/<radius>", methods=["GET"])
def building_users(user_id, radius):
    from_building = user_building(
        db.User.find_one({
            '_id': user_id
        })['cur_pos'])
    if not from_building:
        return ("", 204)
    in_building = db.User.find({
        'cur_pos': {
            '$near': {
                '$geometry': {
                    'type': 'Point',
                    'coordinates': from_building['position']
                },
                '$maxDistance': float(radius)
            }
        }
    })
    in_building = [x for x in in_building if x['_id'] != user_id]
    return (
        dumps(in_building),
        200,
        {
            "ContentType": "application/json"
        },
    )


@mod_user.route("/<user_id>/nearby/<range>", methods=["GET"])
def api_nearby_users(user_id, range):
    user_table = get_users_in_range(user_id, range)
    if not user_table:
        return ("", 204)
    return (
        dumps(user_table),
        200,
        {
            "ContentType": "application/json"
        },
    )
