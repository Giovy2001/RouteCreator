from flask import render_template
from __main__ import app, database_handler

@app.route("/route/<int:route_id>")
def view_route(route_id):
    route_object = database_handler.get_route(route_id)
    holds_array  = database_handler.get_holds(route_id)

    return render_template("view.html",
        route_name=route_object[1],
        author=route_object[2],
        image=route_object[3],
        description=route_object[4],
        holds=holds_array
    )