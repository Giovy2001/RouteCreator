from flask import redirect, render_template, request, url_for
from scripts import database_handler, image_handler
import json

def view_route(route_id):
    route_object = database_handler.get_route(route_id)
    holds_array  = database_handler.get_holds(route_id)

    if request.method == "POST":
        if 'authorName' in request.form:
            return redirect(url_for(f"edit_name_description", route_id=route_object[0], route_object=json.dumps(route_object)))
            
        elif 'authorHolds' in request.form:
            return redirect(url_for(f"edit_holds", route_id=route_object[0], holds_array=json.dumps(holds_array), image_url=route_object[3]))
            
        elif 'authorDelete' in request.form:
            image_url = route_object[3]
            image_handler.delete(image_url)
            database_handler.del_route(image_url)
            return redirect(url_for("index"))

    return render_template("view.html",
        route=route_object,
        holds=holds_array
    )