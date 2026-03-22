from flask import render_template
from scripts.database_sql import sql_routes
import global_values

def index():
    routes = sql_routes.get_all_routes(global_values.conn)
    return render_template("index.html", routes=routes)

def use_condition():
    return render_template("use_condition.html")