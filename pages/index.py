from flask import render_template
from scripts import database_handler

def index():
    return render_template("index.html", routes=database_handler.get_all_routes())