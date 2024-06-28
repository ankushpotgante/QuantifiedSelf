import os
from flask import Flask
from flask_restful import Api
from application.database import db
from application.config import LocalDevelopmentConfig, ProductionDevelopmentConfig
from flask_cors import CORS
from application import workers

app = None
api = None
celery = None

def create_app():
    app = Flask(__name__, template_folder="templates")

    if os.getenv('ENV', 'development') == 'production':
        print("Starting production config...")
        app.config.from_object(ProductionDevelopmentConfig)
    else:
        print("Starting local config...")
        app.config.from_object(LocalDevelopmentConfig)

    db.init_app(app)
    api = Api(app)
    app.app_context().push()

    celery = workers.celery

    celery.conf.update(
        broker_url = app.config["CELERY_BROKER_URL"],
        result_backend = app.config["CELERY_RESULT_BACKEND"],
        # enable_utc = False,
        # timezone = "Asia/Kolkata"
    )

    celery.Task = workers.ContextTask

    app.app_context().push()

    app.app_context().push()


    return app, api, celery


app, api, celery = create_app()
app.secret_key = "mysecret_very_very_secret_key"

CORS(app)

# importing all controllers

from application.controllers import *

# import all resources

from application.resources import UserResource, TrackerResource, LogResource, UserListResource, TrackerListResource, LogListResource

api.add_resource(UserResource, "/api/user", "/api/user/<int:uid>")
api.add_resource(TrackerResource, "/api/tracker", "/api/tracker/<int:tid>")
api.add_resource(LogResource, "/api/log", "/api/log/<int:lid>")
api.add_resource(UserListResource, "/api/users")
api.add_resource(TrackerListResource, "/api/user/trackers", "/api/user/<int:uid>/trackers")
api.add_resource(LogListResource, "/api/tracker/<int:tid>/logs")

if __name__ == '__main__':
    db.create_all()
    app.run()
