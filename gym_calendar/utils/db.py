import sqlite3
import click
import os
from flask import g, Flask, current_app

def open_db():
    if 'db' not in g:
        g.db = sqlite3.connect(current_app.config["DATABASE"], detect_types=sqlite3.PARSE_DECLTYPES)
        g.db.row_factory = sqlite3.Row
    return g.db

def close_db(e):
    db = g.pop("db", None)
    if db is not None:
        db.close()

def create_db():
    db = open_db()

    with current_app.open_resource(os.path.join(current_app.instance_path, "init_schema.sql")) as i_f:
        db.executescript(i_f.read().decode("utf8"))

@click.command("create_db")
def create_db_command():
    create_db()
    click.echo("***DB initialized***")

def initialize_db(app: Flask):
    app.teardown_appcontext(close_db)
    app.cli.add_command(create_db_command)
