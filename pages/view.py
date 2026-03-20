from flask import redirect, render_template, request, url_for
from scripts import database_handler, image_handler

def view_route(route_id):
    route_object = database_handler.get_route(route_id)
    holds_array  = database_handler.get_holds(route_id)

    if request.method == "POST":
        if 'authorName' in request.form:
            ...
            print("name")
            
        elif 'authorHolds' in request.form:
            ...
            print("Holds")
            
        elif 'authorDelete' in request.form:
            image_url = route_object[3]
            image_handler.delete(image_url)
            database_handler.del_route(image_url)
            return redirect(url_for("index"))

    return render_template("view.html",
        route=route_object,
        holds=holds_array
    )