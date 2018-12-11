from app import db
import datetime


class UserMessage(db.Model):
    from_istID = db.Column(db.String(9), primary_key=True)
    sentstamp = db.Column(
        db.DateTime, primary_key=True)  # timestamp given by server
    radius = db.Column(db.Float)
    content = db.Column(db.Text)


class User(db.Model):
    __tablename__ = 'users'
    # Columns
    ist_ID = db.Column(db.String(9), primary_key=True)
    cur_pos_lat = db.Column(db.Float)
    cur_pos_long = db.Column(db.Float)
    building_ID = db.Column(db.BigInteger)
    last_seen = db.Column(db.DateTime, default=datetime.datetime.now)

    # inBuilding query: SELECT buildingID from Building B, User U where
    # sqrt((U.cur_pos_lat - B.location_lat)^2
    # + (U.cur_pos_lat - B.location_lat)^2) < radius

    def __repr__(self):
        return '<User %r>' % (self.ist_ID)


class Building(db.Model):
    building_ID = db.Column(db.BigInteger, primary_key=True)
    location_lat = db.Column(db.Float)
    location_long = db.Column(db.Float)
    name = db.Column(db.String(128))


class Stay(db.Model):
    ist_ID = db.Column(db.String(9), primary_key=True)
    arrival = db.Column(db.DateTime, primary_key=True)
    departure = db.Column(db.DateTime)
    buildingID = db.Column(db.BigInteger)


class BotMessage(db.Model):
    to_buildingID = db.Column(db.BigInteger, primary_key=True)
    sentstamp = db.Column(db.DateTime, primary_key=True)
    content = db.Column(db.Text)
    bot_ID = db.Column(db.Integer, primary_key=True)
