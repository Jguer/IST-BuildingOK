import json

from flask import Blueprint, Flask, jsonify, request

from app import db

mod_bot = Blueprint("bot", __name__, url_prefix="/bot")


@mod_bot.route("/register", methods=["POST"])
def check_online_users():
    online_table = get_users_online()
    if not online_table:
        return ("", 204)
    return json.dumps(jsonify(online_table)), 200, {
        "ContentType": "application/json"
    }
