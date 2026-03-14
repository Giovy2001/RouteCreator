from flask import Flask, render_template, request, redirect, url_for
import json

app = Flask(__name__)

from scripts import database_handler

from scripts import image_handler


@app.route("/")
def index():
    return render_template("index.html", routes=database_handler.get_routes())

@app.route("/create", methods=["GET", "POST"])
def create():
    if request.method == "POST":

        image = request.files["image"]
        holds = request.form["holds"]

        image_url = image_handler.put(image.filename, image.read())

        database_handler.add_route(image_url, holds)

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
