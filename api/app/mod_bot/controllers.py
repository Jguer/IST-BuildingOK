import json

from flask import Blueprint, Flask, jsonify, request
from datetime import datetime
from app import db

mod_bot = Blueprint("bot", __name__, url_prefix="/bot")

@mod_bot.route("/register", methods=["POST"])
def register_bot():
    pass

def check_online_users():
    online_table = db.User.find({'last_seen': {'$gt': datetime.utcnow() - timedelta(minutes = 10)}})
    if not online_table:
        return ("", 204)
    return json.dumps(jsonify(online_table)), 200, {
        "ContentType": "application/json"
    }
