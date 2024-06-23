from application.database import db


class User(db.Model):
    uid = db.Column(db.Integer, primary_key=True, autoincrement=True)
    first_name = db.Column(db.String, nullable=False)
    last_name = db.Column(db.String)
    username = db.Column(db.String, unique=True, nullable=False)
    password = db.Column(db.String, nullable=False)

    trackers = db.relationship('Tracker', backref='usr', lazy='dynamic',
                               cascade='all, delete-orphan', passive_deletes=True)


class Tracker(db.Model):
    tid = db.Column(db.Integer, primary_key=True, autoincrement=True)
    uid = db.Column(db.Integer, db.ForeignKey(
        'user.uid', ondelete='CASCADE'), nullable=False)
    name = db.Column(db.String, nullable=False)
    description = db.Column(db.String)
    tracker_type = db.Column(db.String, nullable=False)
    settings = db.Column(db.String)

    logs = db.relationship('Log', backref='trkr', lazy='dynamic',
                           cascade='all, delete-orphan', passive_deletes=True)


class Log(db.Model):
    lid = db.Column(db.Integer, primary_key=True, autoincrement=True)
    tid = db.Column(db.Integer, db.ForeignKey(
        'tracker.tid', ondelete='CASCADE'), nullable=False)
    log_time = db.Column(db.TIMESTAMP, server_default=db.func.now())
    value = db.Column(db.String)
    notes = db.Column(db.String)
