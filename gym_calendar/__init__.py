import json
import os
import sys
from flask import Flask

def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)

    os.makedirs(app.instance_path, exist_ok=True)
    app.config.from_mapping({
        "SECRET_KEY":"dev",
        "DATABASE":os.path.join(app.instance_path, "calendar_db_local.sqlite")
    })

    if test_config:
        app.config.from_mapping(test_config)
    else:
        app.config.from_pyfile(os.path.join(app.instance_path, "config.py"), silent=True)

    @app.get("/healthcheck")
    def healthcheck():
        return json.dumps({"status": "OK"})

    from gym_calendar.utils import db
    db.initialize_db(app)

    from gym_calendar.blueprints import auth, calendar
    app.register_blueprint(auth.bp)
    app.register_blueprint(calendar.bp)

    return app
