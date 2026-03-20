from flask import redirect, render_template, request, url_for
from scripts import database_handler, image_handler
import json

def edit_holds(route_id):
    image_url = request.args.get("image_url")
    holds_array = json.loads(request.args.get("holds_array"))
    
    if request.method == "POST":
        holds = request.form.get("jsonHolds")
        
        holds_array = []
        for hold_helement in json.loads(holds):
            holds_array.append(hold_helement["data"])
        
        database_handler.edit_holds(route_id, holds_array)
        
        return redirect(url_for("view_route", route_id=route_id))

    return render_template("create_route.html", data={"image_url":image_url,"holds_array":holds_array})


def edit_name_description(route_id):
    route_object = json.loads(request.args.get("route_object"))
    
    if request.method == "POST":
        name = request.form.get("routeName")
        description = request.form.get("routeDescription")
            
        if not name:
            return render_template("save_route.html")
        
        database_handler.edit_name_description(route_id, name, description)
        
        return redirect(url_for("view_route", route_id=route_id))
    
    return render_template("save_route.html", route_object=route_object)