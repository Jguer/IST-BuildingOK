import json

from flask import Blueprint, Flask, jsonify, request
from datetime import datetime, timedelta
from app import db, utils

mod_bot = Blueprint("bot", __name__, url_prefix="/bot")


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


@mod_bot.route("/register", methods=["POST"])
def register_bot():
    content = request.get_json()
    building_id = db.Building.find_one({'name': content['building_ID']})['_id']
    db.Bot.insert_one({'_id': content['id'], 'building_ID': building_id})
    return ("", 200)


@mod_bot.route("/<bot_id>/message", methods=["POST"])
def send_message(bot_id):
    content = request.get_json()
    build = db.Bot.find_one({'_id': bot_id})['building_ID']
    build_pos = db.Building.find_one({'_id': build})['position']
    build_full = db.Building.find_one({'_id': build})
    list_in_range = list(
        db.User.find({
            'cur_pos': {
                '$near': {
                    '$geometry': {
                        'type': 'Point',
                        'coordinates': build_pos
                    },
                    '$maxDistance': utils.default_range
                }
            },
            'last_seen': {
                '$gt': datetime.utcnow() - timedelta(minutes=10)
            }
        }))
    new_messages = [{
        'from_istID': bot_id,
        'sentstamp': datetime.utcnow(),
        'content': content['content'],
        'sent_from': build_full,
        'to_istID': x['_id'],
        'sent_to': user_building(x['cur_pos'])['_id']
    } for x in list_in_range]
    result = db.Message.insert_many(new_messages)
    if (len(result.inserted_ids) == len(new_messages)):
        return jsonify({'result': 'True'}), 200
    return jsonify({'result': 'False'}), 200
