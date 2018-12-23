from flask import Blueprint, request, jsonify
from datetime import datetime, timedelta
from bson.json_util import dumps

from app import db, utils

mod_user = Blueprint("user", __name__, url_prefix="/user")


def get_users_in_range(user_id, radius):
    sending_user = db.User.find_one({'_id': user_id})
    list_in_range = db.User.find({
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
    return list_in_range


def user_building(user_loc):
    list_cur_buildings = [ob.__dict__ for ob in db.Building.find({
        'position': {
            '$near': {
                '$geometry': {
                    "type": 'Point',
                    "coordinates": user_loc
                },
                '$maxDistance': utils.default_range
            }
        }
    })]
    print(list_cur_buildings)
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
    print(cur_pos)
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
    cur_building = user_building(cur_pos)['_id']
    list_last_buildings = db.Activity.find({
        'ist_ID': user_id,
        'departure': lastseen
    })
    last_building = list_last_buildings[0].__dict__['_id']
    if cur_building == last_building:
        db.Activity.update_one({
            'ist_ID': user_id,
            'building_ID': cur_building
        }, {'$currentDate': {
            'departure': True
        }})
    else:
        db.Activity.insert_one({
            'ist_ID': user_id,
            'building_ID': cur_building,
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
        list_nearby_users = [
            x.__dict__['_id']
            for x in get_users_in_range(user_id, cont['radius'])
        ]
        new_messages = [{
            'from_istID':
            user_id,
            'sentstamp':
            datetime.utcnow(),
            'content':
            cont['content'],
            'sent_from':
            from_building,
            'to_istID':
            x.__dict__['_id'],
            'sent_to':
            user_building(x.__dict__['cur_pos'])['_id']
        } for x in list_nearby_users]
        result = db.Message.insert_many(new_messages)
        if (len(result.inserted_ids) == len(new_messages)):
            return jsonify({'result': 'True'}), 200
        return jsonify({'result': 'False'}), 200
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
                '$maxDistance': radius
            }
        }
    })
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
