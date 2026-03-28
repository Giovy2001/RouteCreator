from flask import render_template
from scripts.database_sql import sql_routes
import global_values

def render_use_condition():
    return render_template("use_condition.html")