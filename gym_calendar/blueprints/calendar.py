import re
import json
import os
from flask import (
    Blueprint, render_template, redirect, url_for, request, g
)
from gym_calendar.blueprints.auth import check_request_auth
from gym_calendar.utils.bot import GymBot
from gym_calendar.utils.firebase import get_db
from functools import reduce

bp = Blueprint("calendar", __name__, url_prefix="/calendar")

@bp.get("/")
@check_request_auth
def index():
    return render_template("calendar/index.html")

@bp.get("/history/")
@check_request_auth
def history():
    db = get_db()
    doc_ref = db.collection("programs").document(g.user.uid)
    doc = doc_ref.get().to_dict()
    if not doc or not "program" in doc or doc["program"] == "":
        return []
    else:
        parsed_program = json.loads(doc["program"])
        history_events = filter(lambda x: x["role"] == "assistant", parsed_program)

    merged = reduce(lambda x, y: json.loads(x["content"]) + json.loads(y["content"]), history_events)
    return merged

@bp.post("/bot/")
@check_request_auth
def bot():
    if os.environ.get("LOCAL") == "true":
        bot = GymBot()
    else:
        token = os.environ["DEEPSEEK_API_KEY"]
        bot = GymBot("deepseek-chat", token)

    db = get_db()
    doc_ref = db.collection("programs").document(g.user.uid)
    doc = doc_ref.get().to_dict()

    msg = request.form["msg"]
    if not doc or not "program" in doc or doc["program"] == "":
        res = bot.chat_with_bot(msg, [])
    else:
        res = bot.chat_with_bot(msg, json.loads(doc["program"]))
    c_content = re.sub(r"<think>.*?</think>\n?", "", res[0], flags=re.DOTALL)
    c_content = re.sub(r"^\s*```json\n?", "", c_content)
    c_content = re.sub(r"\n?```\s*$", "", c_content)

    all_messages = res[1]
    doc_ref.set({"program": json.dumps(all_messages)})

    return c_content
