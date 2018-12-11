import json

from flask import Blueprint, Flask, jsonify, request

from app import db
import app.models as models
import datetime

from sqlalchemy import (Column, Integer, String, Boolean, ForeignKey, DateTime,
                        Sequence, Float)
mod_admin = Blueprint("admin", __name__, url_prefix="/admin")


@mod_admin.route("/online", methods=["GET"])
def check_online_users():
    current_time = datetime.datetime.now()
    online_table = db.query(models.User).filter(
        models.User.lastseen > current_time - datetime.timedelta(minutes=10))
    if not online_table:
        return ("", 204)
    return json.dumps(jsonify(online_table)), 200, {
        "ContentType": "application/json"
    }


@mod_admin.route("/building", methods=["GET", "POST"])
def buildings():
    if request.method == "GET":
        buildings_table = db.query(models.Building)
        return (
            json.dumps(jsonify(buildings_table)),
            200,
            {
                "ContentType": "application/json"
            },
        )

    content = request.get_json()
    for i in content:
        b = models.Building(
            building_ID=id,
            location_lat=i["lat"],
            location_long=i["lng"],
            name=i["name"])
        print("building created", b)
        db.session.add(b)
    db.session.commit()
    return json.dumps({
        "success": True
    }), 200, {
        "ContentType": "application/json"
    }


@mod_admin.route("/users/<build_id>", methods=["GET"])
def users_inside(build_id):
    inside_table = get_users_online()
    if not inside_table:
        return ("", 204)
    return json.dumps(jsonify(inside_table)), 200, {
        "ContentType": "application/json"
    }


@mod_admin.route("/users", methods=["GET"])
def show_users():
    online_table = get_users_online()
    if not online_table:
        return ("", 204)
    return json.dumps(jsonify(online_table)), 200, {
        "ContentType": "application/json"
    }


@mod_admin.route("/log/user/<usr_id>", methods=["GET"])
def user_log(usr_id):
    all_usr_actions = get_users_online()
    if not all_usr_actions:
        return ("", 204)
    return (
        json.dumps(jsonify(all_usr_actions)),
        200,
        {
            "ContentType": "application/json"
        },
    )


@mod_admin.route("/log/building/<build_id>", methods=["GET"])
def build_log(build_id):
    all_build_actions = get_users_online()
    if not all_build_actions:
        return ("", 204)
    return (
        json.dumps(jsonify(all_build_actions)),
        200,
        {
            "ContentType": "application/json"
        },
    )
