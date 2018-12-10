from app import db


class User(db.Model):
    # Columns
    ist_ID = db.Column(db.String(9), primary_key=True)
    cur_pos_lat = db.Column(db.Float)
    cur_pos_long = db.Column(db.Float)
    last_seen = db.Column(db.DateTime)
    # inBuilding query: SELECT buildingID from Building B, User U where sqrt((U.cur_pos_lat - B.location_lat)^2 + (U.cur_pos_lat - B.location_lat)^2) < radius
