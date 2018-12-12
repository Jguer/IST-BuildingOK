from flask import jsonify, request
from app import db
import datetime


def building_put():
    content = request.json
    to_add = []
    for i in content:
        to_add.append({
            'location_lat': i["lat"],
            'location_long': i["lng"],
            'name': i["name"]
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
    compare = datetime.datetime.now() - datetime.timedelta(minutes=10)
    online_table = db.User.find({"last_seen": {"$lt": compare}})
    return jsonify([ob.__dict__ for ob in online_table])


def users_inside(build_id):
    compare = datetime.datetime.now() - datetime.timedelta(minutes=10)
    online_table = db.User.find({"last_seen": {"$lt": compare}})
    return jsonify([ob.__dict__ for ob in online_table])
