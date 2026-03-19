from flask import render_template
from scripts import database_handler

def index():
    routes = database_handler.get_all_routes()    
    return render_template("index.html", routes=routes)

def use_condition():
    return render_template("use_condition.html")