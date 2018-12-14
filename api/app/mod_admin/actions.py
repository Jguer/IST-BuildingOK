from flask import jsonify, request
from app import db, utils
import datetime


def building_put():
    content = request.json
    to_add = []
    for i in content:
        to_add.append({
            'id' : i['id'],
            'name': i['name'],
            'position': i['position']
        })
    print(to_add)

    result = db.Building.insert_many(to_add)
    if (len(result.inserted_ids) == len(to_add)):
        return jsonify({'result': 'True'}), 200

    return jsonify({'result': 'False'}), 200


def building_list():
    all_buildings_table = db.Building.find({})
    return jsonify([ob.__dict__ for ob in all_buildings_table])


def online_users():
    compare = datetime.datetime.utcnow() - datetime.timedelta(minutes=10)
    online_table = db.User.find({'last_seen': {'$gt': compare}})
    return jsonify([ob.__dict__ for ob in online_table])


def users_inside(build_id):
    compare = datetime.datetime.utcnow() - datetime.timedelta(minutes=10)
    build_pos = db.Building.find_one({'id': build_id})['position']
    online_table = db.User.find({'last_seen': {'$gt': compare}, cur_pos: {$near: {$geometry: {type: 'Point', coordinates: build_pos},
     $maxDistance: utils.default_range}}})
    return jsonify([ob.__dict__ for ob in online_table])
