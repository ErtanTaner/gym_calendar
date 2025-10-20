import json
import os
import sys
from flask import Flask
from dotenv import load_dotenv
from firebase_admin import initialize_app
from gym_calendar.utils.firebase import init_firebase, get_auth

def create_app(test_config=None):
    load_dotenv()
    app = Flask(__name__, instance_relative_config=True)

    os.makedirs(app.instance_path, exist_ok=True)
    app.config.from_mapping({
        "SECRET_KEY":"dev",
    })

    if test_config:
        app.config.from_mapping(test_config)
    else:
        fname = os.path.join(app.instance_path, "config.py")
        if not os.path.isfile(fname):
            with open(fname, "w") as f:
                f.write(f"SECRET_KEY = '{os.environ.get('SECRET_KEY')}'")
        app.config.from_pyfile(os.path.join(app.instance_path, "config.py"), silent=True)

    @app.get("/healthcheck/")
    def healthcheck():
        return json.dumps({"status": "OK"})

    init_firebase()
    from gym_calendar.blueprints import calendar, auth
    app.register_blueprint(auth.bp)
    app.register_blueprint(calendar.bp)

    return app
