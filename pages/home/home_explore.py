from flask import render_template
from scripts.database_sql import sql_routes
import global_values

def render_home_explore():
    return render_template("home/explore.html")
