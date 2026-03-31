from flask import redirect, render_template, request, url_for
from scripts import image_handler
from scripts.database_sql import sql_routes, sql_holds
import json
import global_values

def view_route(route_id):
    route_object: dict = sql_routes.get_route(global_values.conn, route_id)
    holds_array: list[dict]  = sql_holds.get_holds(global_values.conn, route_id)

    if request.method == "POST":
        if 'authorName' in request.form:
            return redirect(url_for(f"edit_name_description", route_id=route_object["route_id"], route_object=json.dumps(route_object)))
            
        elif 'authorHolds' in request.form:
            return redirect(url_for(f"edit_holds", route_id=route_object["route_id"], holds_array=json.dumps(holds_array), image_url=route_object["image_url"]))
            
        elif 'authorDelete' in request.form:
            image_handler.delete(route_object["image_url"])
            sql_routes.del_route(global_values.conn, route_object["route_id"])
            return redirect(url_for("render_home_archive"))

    return render_template("view.html",
        route=route_object,
        holds=holds_array
    )