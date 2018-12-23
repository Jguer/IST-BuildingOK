import json

from flask import Blueprint, Flask, jsonify, request
from datetime import datetime
from app import db

mod_bot = Blueprint("bot", __name__, url_prefix="/bot")


@mod_bot.route("/register", methods=["POST"])
def register_bot():
    content = request.get_json()
    db.Bot.insert_one({
        '_id': content['id'],
        'building_ID': content['building_ID']
    })
    return ("", 200)


@mod_bot.route("/<bot_id>/message", methods=["POST"])
def send_message(bot_id):
    content = request.get_json()
    build = db.Bot.find_one({'_id': bot_id})['building_ID']
    build_pos = db.Building.find_one({'_id': build_pos})['position']
    list_in_range = list(db.User.find({
        'cur_pos': {
            '$near': {
                '$geometry': {
                    'type': 'Point',
                    'coordinates': build_pos
                },
                '$maxDistance': range,
                '$minDistance': 1
            }
        },
        'last_seen': {
            '$gt': datetime.utcnow() - timedelta(minutes=10)
        }
    }))
    new_messages = [{
        'from_istID':
        bot_id,
        'sentstamp':
        datetime.utcnow(),
        'content':
        content['content'],
        'sent_from':
        build,
        'to_istID':
        x['ist_ID'],
        'sent_to':
        user_building(x['cur_pos'])['_id']
    } for x in list_in_range]
    result = db.Message.insert_many(new_messages)
    if (len(result.inserted_ids) == len(new_messages)):
        return jsonify({'result': 'True'}), 200
    return jsonify({'result': 'False'}), 200
