import json
import functools
from flask import (
    Blueprint, request, g, session, flash, redirect, url_for, render_template
)
from gym_calendar.utils.db import open_db
from werkzeug.security import generate_password_hash, check_password_hash
from secrets import token_hex

bp = Blueprint("auth", __name__, url_prefix="/auth")

@bp.get("/test/")
def auth_test() -> str:
    return json.dumps({"status": "Ok from auth blueprint."})

@bp.route("/register/", methods=("GET", "POST"))
def register():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["username"]
        am = AuthManager(username, password)

        if am.check_credentials():
            am.register()
            return redirect(url_for("calendar.index"))
    return render_template("auth/register.html")

@bp.route("/login/", methods=("GET","POST"))
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        am = AuthManager(username, password)

        if am.check_credentials():
            am.login()
            return redirect(url_for("calendar.index"))
    return render_template("auth/login.html")

@bp.get("/logout/")
def logout():
    session = session.get("session_id")
    db = open_db()
    db.execute(
        "UPDATE users SET session_id = '' WHERE user_id = ?",
        (g.user.user_id)
    )
    return redirect(url_for("auth.login"))

@bp.before_app_request
def get_current_user():
    db = open_db()
    session_id = session.get("session_id")
    if session_id is None:
        g.user = None
    else:
        g.user = db.execute("SELECT * FROM users WHERE session_id = ?", (session_id,)).fetchone()

def check_request_auth(wiew):
    @functools.wrap(wiew)
    def wrapped_wiew(**kwargs):
        if g.user is not None:
            return view(**kwargs)
        else:
            return redirect(url_for("auth.login"))
    return wrapped_wiew


class AuthManager():
    def __init__(self, username: str, password: str):
        self.username = username
        self.password = password

    def register(self) -> None:
        db = open_db()
        db.execute(
            "INSERT INTO users (username, password) VALUES (?, ?)",
            (self.username, generate_password_hash(self.password))
        )
        db.commit()

    def login(self) -> None:
        db = open_db()
        curr_user = db.execute(
            "SELECT * from users WHERE username = ?",
            (self.username)
        ).fetchone()

        if curr_user is None:
            flash("No user found with given input.")
            return None
        elif not check_password_hash(self.password, curr_user.password):
            flash("User information is incorrect.")
            return None

        session_id = token_hex()
        session["session_id"] = session_id
        db.execute(
            "UPDATE users SET session_id = ? WHERE user_id = ?",
            (session_id, curr_user.user_id)
        )
        db.commit()
    def check_credentials(self) -> bool:
        error = None
        if self.username is None:
            error = f"Username is required to create a user."
        elif self.password is None:
            error = f"Password is required to create a user."
        if error is not None:
            flash(error)
            return False
        return True
