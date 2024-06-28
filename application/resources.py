from flask_restful import Resource, reqparse, marshal_with, fields, abort, inputs
from application.models import User, Tracker, Log
from application.database import db
from hashlib import md5
from flask_marshmallow import Marshmallow
from flask import current_app as app, jsonify
from flask_jwt_extended import JWTManager, jwt_required, create_access_token, get_jwt_identity

ma = Marshmallow(app)


# User output
user_output = {
    'uid': fields.Integer,
    'username': fields.String,
    'first_name': fields.String,
    'last_name': fields.String,
    'email': fields.String,
    'password': fields.String,
}

# User request parsers
user_create_req = reqparse.RequestParser()

user_create_req.add_argument('first_name', type=str, help="First name is required and is string", required=True)

user_create_req.add_argument('email', type=str, help="Email is required and is string", required=True)

user_create_req.add_argument('last_name', type=str, help="Last name is string")

user_create_req.add_argument('username', type=str, help="Username is required and is string", required=True)

user_create_req.add_argument('password', type=str, help="Password is required and is string", required=True)


user_update_req = reqparse.RequestParser()

user_update_req.add_argument('first_name', type=str, help="First name is required and is string", required=True)

user_update_req.add_argument('last_name', type=str, help="Last name is required and is string", required=True)


# User resource
class UserResource(Resource):

    @jwt_required()
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
                    email=data.email, username=data.username, password=passwd)
        if user:
            db.session.add(user)
            db.session.commit()
            return user
        else:
            abort(500, message="Something went wrong!")

    @jwt_required()
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
            return jsonify(message="User deleted successfully!")
        else:
            abort(404, message="User not found!")

    @jwt_required()
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


class UserSchema(ma.Schema):
    class Meta:
        fields = ('uid', 'username', 'first_name', 'last_name', 'email', 'password')


users_schema = UserSchema(many=True)


class UserListResource(Resource):

    @jwt_required()
    def get(self):

        users = User.query.all()

        if users:
            
            result = users_schema.dump(users)
            return jsonify(result)

        else:
            abort(404, message="No user found")


# Tracker output
tracker_output = {
    'tid': fields.Integer,
    'uid': fields.Integer,
    'name': fields.String,
    'description': fields.String,
    'tracker_type': fields.String,
    'last_tracked': fields.DateTime,
    'settings': fields.String
}

# Tracker request parsers
tracker_create_req = reqparse.RequestParser()
tracker_create_req.add_argument(
    'uid', type=int, help="uid required and is Integer", required=True)
tracker_create_req.add_argument(
    'name', type=str, help="name required and is string", required=True)
tracker_create_req.add_argument(
    'description', type=str, help="description is string")
tracker_create_req.add_argument(
    'tracker_type', type=str, help="tracker_type required and is string", required=True)
tracker_create_req.add_argument(
    'settings', type=str, help="settings and is string")

tracker_update_req = reqparse.RequestParser()
# tracker_update_req.add_argument('name', type=str, help="name required and is string", required=True)
tracker_update_req.add_argument(
    'description', type=str, help="description is string")
tracker_update_req.add_argument(
    'tracker_type', type=str, help="tracker_type required and is string", required=True)
tracker_update_req.add_argument(
    'settings', type=str, help="settings and is string")


# Tracker resource
class TrackerResource(Resource):

    @jwt_required()
    @marshal_with(tracker_output)
    def get(self, tid):
        tracker = Tracker.query.get(tid)

        if tracker:
            if tracker.uid == get_jwt_identity():
                return tracker
            else:
                abort(403, message="Unauthorised access to tracker!")
        else:
            abort(404, message="Tracker not found!")

    @jwt_required()
    @marshal_with(tracker_output)
    def post(self):
        data = tracker_create_req.parse_args()
        u = User.query.get(data.uid)
        if u and u.uid == get_jwt_identity():
            tracker = Tracker(uid=data.uid, name=data.name, description=data.description,
                              tracker_type=data.tracker_type, settings=data.settings)
            db.session.add(tracker)
            db.session.commit()
            return tracker
        else:
            abort(400, message='Enter correct user id')

    @jwt_required()
    def delete(self, tid):
        tracker = Tracker.query.get(tid)
        if tracker:
            if tracker.uid == get_jwt_identity():
                Log.query.filter(Log.tid == tracker.tid).delete()
                db.session.delete(tracker)
                db.session.commit()
                return jsonify(message="Tracker deleted successfully!")
            else:
                abort(403, message="Unauthorised access to tracker!")
            
        else:
            abort(404, message="Tracker not found!")

    @jwt_required()
    @marshal_with(tracker_output)
    def put(self, tid):
        tracker = Tracker.query.get(tid)
        if tracker:
            if tracker.uid == get_jwt_identity():
                data = tracker_update_req.parse_args()
                tracker.tracker_type = data.tracker_type
                tracker.description = data.description
                tracker.settings = data.settings
                db.session.add(tracker)
                db.session.commit()
                return tracker
            else:
                abort(403, message="Unauthorised access to tracker!")
            
        else:
            abort(404, message="Tracker not found!")


class TrackerSchema(ma.Schema):
    class Meta:
        fields = ('tid', 'uid', 'name', 'description', 'tracker_type', 'last_tracked', 'settings')


trackers_schema = TrackerSchema(many=True)


class TrackerListResource(Resource):

    @jwt_required()
    def get(self, uid=""):

        if not uid:
            uid = get_jwt_identity()

        trackers = Tracker.query.filter_by(uid=uid).all()

        if trackers:

            result = trackers_schema.dump(trackers)
            return jsonify(result)

        else:
            abort(404, messsage="No trackers found")


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
log_create_req.add_argument(
    'tid', type=int, help="tid required and is string", required=True)
# log_create_req.add_argument('log_time', type=inputs.datetime_from_iso8601, help="log_time required and is datetime", required=True)

log_create_req.add_argument(
    'value', type=str, help="value is required is string", required=True)

log_create_req.add_argument('notes', type=str, help="notes is string")

log_update_req = reqparse.RequestParser()
# log_update_req.add_argument('log_time', type=inputs.datetime_from_iso8601, help="log_time required and is datetime", required=True)

log_update_req.add_argument(
    'value', type=str, help="value is required is string", required=True)

log_update_req.add_argument('notes', type=str, help="notes is string")


# Log resource
class LogResource(Resource):

    @jwt_required()
    @marshal_with(log_output)
    def get(self, lid):
        log = Log.query.get(lid)
        if log:
            return log
        else:
            abort(404, message="Log not found!")

    @jwt_required()
    @marshal_with(log_output)
    def post(self):
        data = log_create_req.parse_args()
        t = Tracker.query.get(data.tid)
        if t:
            if t.tracker_type == "Numeric":
                try:
                    temp = float(data.value)
                except TypeError:
                    abort(400, message="Invalid tracker value")

            if t.tracker_type == "Multiple Choice":
                options = [i.strip() for i in t.settings.split(",")]
                if data.value not in options:
                    abort(400, message="Invalid tracker value")

            if t.tracker_type == "Boolean":
                if data.value not in ["Yes", "No"]:
                    abort(400, message="Invalid tracker value")

            l = Log(tid=t.tid, value=data.value, notes=data.notes)
            db.session.add(l)
            db.session.flush()
            t.last_tracked = l.log_time
            db.session.add(t)
            db.session.commit()
            return l
        else:
            abort(400, message="Enter correct tracker id")

    @jwt_required()
    def delete(self, lid):
        log = Log.query.get(lid)
        if log:
            db.session.delete(log)
            db.session.commit()
            return jsonify(message="log deleted successfully!")
        else:
            abort(404, message="Log not found!")

    @jwt_required()
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


class LogSchema(ma.Schema):
    class Meta:
        fields = ('lid', 'tid', 'log_time', 'value', 'notes')


logs_schema = LogSchema(many=True)


class LogListResource(Resource):

    @jwt_required()
    def get(self, tid):

        logs = Log.query.filter_by(tid=tid).all()

        if logs:

            result = logs_schema.dump(logs)
            return jsonify(result)

        else:

            abort(404, message="No logs found")

