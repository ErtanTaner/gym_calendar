import json
import functools
import click
import os
from flask import (
    Blueprint, request, g, session, flash, redirect, url_for, render_template, current_app
)
from secrets import token_hex
from gym_calendar.utils.firebase import get_db, get_auth

bp = Blueprint("auth", __name__, url_prefix="/auth")

@bp.get("/test/")
def auth_test() -> str:
    return json.dumps({"status": "Ok from auth blueprint."})

@bp.route("/register/", methods=("GET", "POST"))
def register():
    if request.method == "POST":
        email = request.form["email"]
        am = AuthManager(email)

        if am.check_credentials():
            am.register()
            return redirect(url_for("auth.login"))
    return render_template("auth/register.html")

@bp.route("/login/", methods=("GET","POST"))
def login():
    if request.method == "POST":
        email = request.form["email"]
        am = AuthManager(email)

        if am.check_credentials():
            am.login()
            return redirect(url_for("calendar.index"))
    return render_template("auth/login.html")

@bp.post("/logout/")
def logout():
    session_id = session.pop("session_id", None)
    if session_id is not None:
        del g.user 
    return redirect(url_for("auth.login"))

@bp.before_app_request
def get_current_user():
    id = session.get("session_id")
    if id is None:
        g.user = None
    else:
        auth = get_auth()
        user = auth.get_user(id)
        g.user = user

def check_request_auth(view):
    @functools.wraps(view)
    def wrapped_wiew(**kwargs):
        if g.user is not None:
            return view(**kwargs)
        else:
            return redirect(url_for("auth.login"))
    return wrapped_wiew

class AuthManager():
    def __init__(self, email: str) -> None:
        self.email = email

    def register(self) -> None:
        auth = get_auth()
        auth.create_user(
            email=self.email,
            password="66666666",
            disabled=False
        )

    def login(self) -> None:
        auth = get_auth()
        curr_user = auth.get_user_by_email(self.email)

        if curr_user is None:
            flash("No user found with given input.")
            return None

        session["session_id"] = curr_user.uid
    def check_credentials(self) -> bool:
        error = None
        if self.email is None:
            error = f"Email is required to create a user."
        if error is not None:
            flash(error)
            return False
        return True
