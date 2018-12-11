import json

from flask import Blueprint, Flask, jsonify, request

from app import db

mod_user = Blueprint("user", __name__, url_prefix="/user")


@mod_user.route("/<user_id>", methods=["POST"])  # receives an authentication token
def register_user(user_id):
    # login function
    # if the user is not on the database, add him to it
    return ("", 200)


@mod_user.route("/<user_id>/location", methods=["POST"])
def update_loc(user_id):
    content = request.get_json()
    update_coord(content, user_id)
    return json.dumps({"success": True}), 200, {"ContentType": "application/json"}


@mod_user.route("/<user_id>/message", methods=["POST", "GET"])
def message_log(user_id):
    if request.method == "POST":
        content = request.get_json()
        post_message(content, user_id)
        return json.dumps({"success": True}), 200, {"ContentType": "application/json"}
    return sent_messages()


@mod_user.route("/<user_id>/nearby/<range>", methods=["GET"])
def api_nearby_users(user_id, range):
    user_table = get_users_in_range(user_id, range)
    if not user_table:
        return ("", 204)
    return json.dumps(jsonify(user_table)), 200, {
        "ContentType": "application/json"
    }
