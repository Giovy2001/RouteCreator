from flask import redirect, render_template, request, url_for
from scripts import image_handler
from scripts.database_sql import sql_holds, sql_routes
import global_values
import json

def edit_holds(route_id):
    image_url = request.args.get("image_url")
    holds_array = json.loads(request.args.get("holds_array"))
    
    if request.method == "POST":
        holds = request.form.get("jsonHolds")
        
        holds_array = []
        for hold_helement in json.loads(holds):
            holds_array.append(hold_helement["data"])
        
        sql_holds.edit_holds(global_values.conn, route_id, holds_array)
        
        return redirect(url_for("view_route", route_id=route_id))

    return render_template("create_route.html", data={"image_url":image_url,"holds_array":holds_array})


def edit_name_description(route_id):
    route_object = json.loads(request.args.get("route_object"))
    
    if request.method == "POST":
        name = request.form.get("routeName")
        description = request.form.get("routeDescription")
            
        if not name:
            return render_template("save_route.html")
        
        sql_routes.edit_route(global_values.conn, route_id, {"route_name":name, "route_description":description})
        
        return redirect(url_for("view_route", route_id=route_id))
    
    return render_template("save_route.html", route_object=route_object)