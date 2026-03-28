from flask import render_template
from scripts.database_sql import sql_routes
import global_values

def render_home_archive():
    routes = sql_routes.get_all_routes(global_values.conn)
    return render_template("home/archive.html", routes=routes)

# TODO: cambia index nel nuovo file