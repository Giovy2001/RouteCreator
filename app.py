from flask import Flask, render_template, request, redirect, url_for
import os
import json

app = Flask(__name__)
app.config["UPLOAD_FOLDER"] = "static/uploads"

from scripts import database_handler

database_handler.init_db()

@app.route("/")
def index():
    return render_template("index.html", routes=database_handler.get_routes())

@app.route("/create", methods=["GET", "POST"])
def create():
    if request.method == "POST":

        image = request.files["image"]
        holds = request.form["holds"]

        path = os.path.join(app.config["UPLOAD_FOLDER"], image.filename)
        image.save(path)

        database_handler.add_route(image, holds)

        return redirect(url_for("index"))

    return render_template("create.html")

@app.route("/route/<int:id>")
def view(id):

    route = database_handler.get_route(id)

    holds = json.loads(route[2])

    return render_template(
        "view.html",
        image=route[1],
        holds=holds
    )
