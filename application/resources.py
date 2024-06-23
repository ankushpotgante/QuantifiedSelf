from flask_restful import Resource, reqparse, marshal_with, fields, abort, inputs
from application.models import User, Tracker, Log
from application.database import db
from hashlib import md5

# User output
user_output = {
    'uid': fields.Integer,
    'username': fields.String,
    'first_name': fields.String,
    'last_name': fields.String,
    'password': fields.String
}

# User request parsers
user_create_req = reqparse.RequestParser()
user_create_req.add_argument('first_name', type=str, help="First name is required and is string", required=True)
user_create_req.add_argument('last_name', type=str, help="Last name is string")
user_create_req.add_argument('username', type=str, help="Username is required and is string", required=True)
user_create_req.add_argument('password', type=str, help="email is required and is string", required=True)

user_update_req = reqparse.RequestParser()
user_update_req.add_argument('first_name', type=str, help="First name is required and is string", required=True)
user_update_req.add_argument('last_name', type=str, help="Last name is required and is string", required=True)


# User resource
class UserResource(Resource):

    @marshal_with(user_output)
    def get(self, uid):
        user = User.query.get(uid)
        if user:
            return user
        else:
            abort(404, message="User not found!")

    @marshal_with(user_output)
    def post(self):
        data = user_create_req.parse_args()
        password = data.password
        p = md5(password.encode())
        passwd = p.hexdigest()
        user = User(first_name=data.first_name, last_name=data.last_name,
                    username=data.username, password=passwd)
        if user:
            db.session.add(user)
            db.session.commit()
            return user
        else:
            abort(500, message="Something went wrong!")

    def delete(self, uid):
        user = User.query.get(uid)
        if user:
            trackers = user.trackers.all()
            if trackers:
                for tracker in trackers:
                    Log.query.filter(Log.tid == tracker.tid).delete()
                    db.session.delete(tracker)
            db.session.delete(user)
            db.session.commit()
            return "User deleted successfully!"
        else:
            abort(404, message="User not found!")

    @marshal_with(user_output)
    def put(self, uid):
        user = User.query.get(uid)
        if user:
            data = user_update_req.parse_args()
            user.first_name = data.first_name
            user.last_name = data.last_name
            db.session.add(user)
            db.session.commit()
            return user
        else:
            abort(404, message="User not found!")


# Tracker output
tracker_output = {
    'tid': fields.Integer,
    'uid': fields.Integer,
    'name': fields.String,
    'description': fields.String,
    'tracker_type': fields.String,
    'settings': fields.String
}

# Tracker request parsers
tracker_create_req = reqparse.RequestParser()
tracker_create_req.add_argument('uid', type=int, help="uid required and is Integer", required=True)
tracker_create_req.add_argument('name', type=str, help="name required and is string", required=True)
tracker_create_req.add_argument('description', type=str, help="description is string")
tracker_create_req.add_argument('tracker_type', type=str, help="tracker_type required and is string", required=True)
tracker_create_req.add_argument('settings', type=str, help="settings and is string")

tracker_update_req = reqparse.RequestParser()
# tracker_update_req.add_argument('name', type=str, help="name required and is string", required=True)
tracker_update_req.add_argument('description', type=str, help="description is string")
tracker_update_req.add_argument('tracker_type', type=str, help="tracker_type required and is string", required=True)
tracker_update_req.add_argument('settings', type=str, help="settings and is string")


# Tracker resource
class TrackerResource(Resource):

    @marshal_with(tracker_output)
    def get(self, tid):
        tracker = Tracker.query.get(tid)
        if tracker:
            return tracker
        else:
            abort(404, message="Tracker not found!")

    @marshal_with(tracker_output)
    def post(self):
        data = tracker_create_req.parse_args()
        u = User.query.get(data.uid)
        if u:
            tracker = Tracker(uid=data.uid, name=data.name, description=data.description,
                            tracker_type=data.tracker_type, settings=data.settings)
            db.session.add(tracker)
            db.session.commit()
            return tracker
        else:
            abort(400, message='Enter correct user id')

    def delete(self, tid):
        tracker = Tracker.query.get(tid)
        if tracker:
            Log.query.filter(Log.tid == tracker.tid).delete()
            db.session.delete(tracker)
            db.session.commit()
            return "Tracker deleted successfully!"
        else:
            abort(404, message="Tracker not found!")

    @marshal_with(tracker_output)
    def put(self, tid):
        tracker = Tracker.query.get(tid)
        if tracker:
            data = tracker_update_req.parse_args()
            tracker.tracker_type = data.tracker_type
            tracker.description = data.description
            tracker.settings = data.settings
            db.session.add(tracker)
            db.session.commit()
            return tracker
        else:
            abort(404, message="Tracker not found!")


# Tracker output
log_output = {
    'lid': fields.Integer,
    'tid': fields.Integer,
    'log_time': fields.DateTime,
    'value': fields.String,
    'notes': fields.String,
}

# Tracker request parsers
log_create_req = reqparse.RequestParser()
log_create_req.add_argument('tid', type=int, help="tid required and is string", required=True)
# log_create_req.add_argument('log_time', type=inputs.datetime_from_iso8601, help="log_time required and is datetime", required=True)
log_create_req.add_argument('value', type=str, help="value is required is string", required=True)
log_create_req.add_argument('notes', type=str, help="notes is string")

log_update_req = reqparse.RequestParser()
# log_update_req.add_argument('log_time', type=inputs.datetime_from_iso8601, help="log_time required and is datetime", required=True)
log_update_req.add_argument('value', type=str, help="alue is required is string", required=True)
log_update_req.add_argument('notes', type=str, help="notes is string")


# Log resource
class LogResource(Resource):

    @marshal_with(log_output)
    def get(self, lid):
        log = Log.query.get(lid)
        if log:
            return log
        else:
            abort(404, message="Log not found!")

    @marshal_with(log_output)
    def post(self):
        data = log_create_req.parse_args()
        t = Tracker.query.get(data.tid)
        if t:
            log = Log(tid=data.tid, value=data.value, notes=data.notes)
            db.session.add(log)
            db.session.commit()
            return log
        else:
            abort(400, message="Enter correct tracker id")

    def delete(self, lid):
        log = Log.query.get(lid)
        if log:
            db.session.delete(log)
            db.session.commit()
            return "log deleted successfully!"
        else:
            abort(404, message="Log not found!")

    @marshal_with(log_output)
    def put(self, lid):
        log = Log.query.get(lid)
        if log:
            data = log_update_req.parse_args()
            log.value = data.value
            log.notes = data.notes
            db.session.add(log)
            db.session.commit()
            return log
        else:
            abort(404, message="Log not found!")
