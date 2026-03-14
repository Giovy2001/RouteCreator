from flask import Flask, render_template, request, redirect, url_for
import sqlite3
import os
import json

app = Flask(__name__)
app.config["UPLOAD_FOLDER"] = "static/uploads"

def get_db():
    return sqlite3.connect("routes.db")

def init_db():
    db = get_db()
    db.execute("""
    CREATE TABLE IF NOT EXISTS routes(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        image TEXT,
        holds TEXT
    )
    """)
    db.commit()

init_db()

@app.route("/")
def index():
    db = get_db()
    routes = db.execute("SELECT * FROM routes").fetchall()
    return render_template("index.html", routes=routes)

@app.route("/create", methods=["GET", "POST"])
def create():
    if request.method == "POST":

        image = request.files["image"]
        holds = request.form["holds"]

        path = os.path.join(app.config["UPLOAD_FOLDER"], image.filename)
        image.save(path)

        db = get_db()
        db.execute(
            "INSERT INTO routes(image, holds) VALUES (?,?)",
            (image.filename, holds)
        )
        db.commit()

        return redirect(url_for("index"))

    return render_template("create.html")

@app.route("/route/<int:id>")
def view(id):

    db = get_db()
    route = db.execute("SELECT * FROM routes WHERE id=?", (id,)).fetchone()

    holds = json.loads(route[2])

    return render_template(
        "view.html",
        image=route[1],
        holds=holds
    )
