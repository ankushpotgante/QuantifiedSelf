import os
from flask import Flask
from flask_restful import Api
from application.database import db
from application.config import LocalDevelopmentConfig, ProductionDevelopmentConfig

app = None
api = None


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
    return app, api


app, api = create_app()
app.secret_key = "mysecret_very_very_secret_key"

# importing all controllers

from application.controllers import *

# import all resources

from application.resources import UserResource, TrackerResource, LogResource

api.add_resource(UserResource, "/api/user", "/api/user/<int:uid>")
api.add_resource(TrackerResource, "/api/tracker", "/api/tracker/<int:tid>")
api.add_resource(LogResource, "/api/log", "/api/log/<int:lid>")

if __name__ == '__main__':
    db.create_all()
    app.run()
