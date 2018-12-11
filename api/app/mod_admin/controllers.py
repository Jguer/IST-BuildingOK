import json

from flask import Blueprint, Flask, jsonify, request

from app import db

mod_admin = Blueprint("admin", __name__, url_prefix="/admin")


@mod_admin.route("/online", methods=["GET"])
def check_online_users():
    online_table = get_users_online()
    if not online_table:
        return ("", 204)
    return json.dumps(jsonify(online_table)), 200, {"ContentType": "application/json"}


@mod_admin.route("/building", methods=["GET", "POST"])
def buildings():
    if request.method == "GET":
        return (
            json.dumps(jsonify(buildings_table)),
            200,
            {"ContentType": "application/json"},
        )
    content = request.get_json()
    insert_building(content)
    return json.dumps({"success": True}), 200, {"ContentType": "application/json"}


@mod_admin.route("/users/<build_id>", methods=["GET"])
def users_inside(build_id):
    inside_table = get_users_online()
    if not inside_table:
        return ("", 204)
    return json.dumps(jsonify(inside_table)), 200, {"ContentType": "application/json"}


@mod_admin.route("/users", methods=["GET"])
def show_users():
    online_table = get_users_online()
    if not online_table:
        return ("", 204)
    return json.dumps(jsonify(online_table)), 200, {"ContentType": "application/json"}


@mod_admin.route("/log/user/<usr_id>", methods=["GET"])
def user_log(usr_id):
    all_usr_actions = get_users_online()
    if not all_usr_actions:
        return ("", 204)
    return (
        json.dumps(jsonify(all_usr_actions)),
        200,
        {"ContentType": "application/json"},
    )


@mod_admin.route("/log/building/<build_id>", methods=["GET"])
def build_log(build_id):
    all_build_actions = get_users_online()
    if not all_build_actions:
        return ("", 204)
    return (
        json.dumps(jsonify(all_build_actions)),
        200,
        {"ContentType": "application/json"},
    )
