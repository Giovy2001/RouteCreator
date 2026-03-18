from flask import render_template
from scripts import database_handler

def view_route(route_id):
    route_object = database_handler.get_route(route_id)
    holds_array  = database_handler.get_holds(route_id)

    return render_template("view.html",
        route=route_object,
        holds=holds_array
    )