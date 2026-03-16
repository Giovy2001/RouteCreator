from flask import render_template
from __main__ import app, database_handler

@app.route("/")
def index():
    return render_template("index.html", routes=database_handler.get_all_routes())