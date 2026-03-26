from flask import render_template
from scripts.database_sql import sql_routes
import global_values

def render_page():
    return render_template("home/profile.html")