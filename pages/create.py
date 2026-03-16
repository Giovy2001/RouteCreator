from flask import render_template, request, redirect, url_for, session, jsonify
from scripts import image_handler, database_handler
import json

def select_image():
    if request.method == "POST":

        image = request.files["image"]

        image_url = image_handler.put(image.filename, image.read())

        #session['last_uploaded_image_url'] = image_url

        return redirect(url_for("create_route", image_url=image_url))

    return render_template("select_image.html")


def create_route():
    #image_url = session.get('last_uploaded_image_url', None)
    image_url = request.args.get("image_url")
    #if not image_url:
    #    return redirect(url_for("index"))
    
    if request.method == "POST":
        #session['holds'] = request.form.get("jsonHolds")
        #session['last_uploaded_image_url'] = image_url
        holds = request.form.get("jsonHolds")
        
        return redirect(url_for("save_route", image_url=image_url, holds=holds)) 

    return render_template("create_route.html", data={"image_url":image_url})


def save_route():    
    if request.method == "POST":
        #image_url = session.get('last_uploaded_image_url', None)
        #holds = session.get('holds', None)
        image_url = request.args.get("image_url")
        holds = request.args.get("holds")
        
        author = request.form.get("routeAuthor")
        name = request.form.get("routeName")
        description = request.form.get("routeDescription")
    
        holds_array = []
        for hold_helement in json.loads(holds):
            holds_array.append(hold_helement["data"])
            
        if not name:
            return render_template("save_route.html")
        
        database_handler.add_route(name, author if author else "Anonimo", image_url, description if description else "", holds_array)
        
        return redirect(url_for("index"))

    return render_template("save_route.html")