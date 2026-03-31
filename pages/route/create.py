from flask import render_template, request, redirect, url_for, session, jsonify
from scripts import image_handler
from scripts.database_sql import sql_routes
import global_values
import json

def select_image():
    if request.method == "POST":
        image = request.files["image"]
        image_url: str = image_handler.put(image.filename, image.read())

        return redirect(url_for("create_route", image_url=image_url))

    return render_template("select_image.html")


def create_route():
    image_url: str = request.args.get("image_url")
    
    if request.method == "POST":
        holds = request.form.get("jsonHolds")
        
        return redirect(url_for("save_route", image_url=image_url, holds=holds)) 

    return render_template("create_route.html", data={"image_url":image_url})


def save_route():    
    if request.method == "POST":
        route_data: dict = {}
        route_data["route_name"] = request.form.get("routeName")
        route_data["author"] = request.form.get("routeAuthor")
        route_data["route_grade"] = request.form.get("routeGrade")
        route_data["route_description"] = request.form.get("routeDescription")
        route_data["image_url"] = request.args.get("image_url")
        
        if not route_data["route_name"]:
            return render_template("save_route.html")
        
        holds = request.args.get("holds")
        holds_array = [hold["data"] for hold in json.loads(holds)]
        
        sql_routes.add_route(global_values.conn, route_data, holds_array)
        
        return redirect(url_for("render_home_archive"))

    return render_template("save_route.html")