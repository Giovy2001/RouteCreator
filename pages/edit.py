from flask import redirect, render_template, request, url_for
from scripts import database_handler, image_handler
import ast

def edit_holds():
    image_url = request.args.get("image_url")
    
    if request.method == "POST":
        holds = request.form.get("jsonHolds")
        
        return redirect(url_for("save_route", image_url=image_url, holds=holds)) 

    return render_template("create_route.html", data={"image_url":image_url})


def edit_name_description(route_id):
    route_object = request.args.get("route_object")
    
    if request.method == "POST":
        name = request.form.get("routeName")
        description = request.form.get("routeDescription")
            
        if not name:
            return render_template("save_route.html")
        
        database_handler.edit_name_description(route_id, name, description)
        
        return redirect(url_for("view_route", route_id=route_id))
    
    return render_template("save_route.html", route_object=ast.literal_eval(route_object))