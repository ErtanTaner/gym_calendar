from flask import (
    Blueprint, render_template, redirect, url_for, request
)
from gym_calendar.blueprints.auth import check_request_auth
from gym_calendar.utils.bot import GymBot
import asyncio
import re
import json

bp = Blueprint("calendar", __name__, url_prefix="/calendar")

@bp.get("/")
@check_request_auth
def index():
    return render_template("calendar/index.html")

@bp.post("/bot/")
@check_request_auth
def bot():
    bot = GymBot()
    msg = request.form["msg"]
    res = bot.chat_with_bot(msg)
    c_content = re.sub(r"<think>.*?</think>\n?", "", res["message"]["content"], flags=re.DOTALL)
    return json.dumps(c_content)
