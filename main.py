from flask import Flask

app = Flask(__name__)

import global_values
global_values.load_database()

if __name__ != "__main__":
    global_values.RUN_LOCALLY, global_values.RUN_LOCALLY = False

from pages.route import create, view, edit
from pages.home import home_explore, home_profile, home_archive
from pages import use_condition

app.add_url_rule("/",                           view_func=home_explore.render_home_explore)
app.add_url_rule("/profile",                    view_func=home_profile.render_home_profile, methods=["GET", "POST"])
app.add_url_rule("/create_user",                view_func=home_profile.render_create_user,  methods=["GET", "POST"])
app.add_url_rule("/archive",                    view_func=home_archive.render_home_archive)
app.add_url_rule("/use_condition",              view_func=use_condition.render_use_condition)

app.add_url_rule("/route_<int:route_id>",       view_func=view.view_route,              methods=["GET", "POST"])
app.add_url_rule("/edit_route_<int:route_id>",  view_func=edit.edit_name_description,   methods=["GET", "POST"])
app.add_url_rule("/edit_holds_<int:route_id>",  view_func=edit.edit_holds,              methods=["GET", "POST"])

app.add_url_rule("/select_image",               view_func=create.select_image,          methods=["GET", "POST"])
app.add_url_rule("/create_route",               view_func=create.create_route,          methods=["GET", "POST"])
app.add_url_rule("/save_route",                 view_func=create.save_route,            methods=["GET", "POST"])

# Backends
from pages.backend import backend_profile

app.add_url_rule("/backend_update_color",       view_func=backend_profile.update_color, methods=["POST"])


if __name__ == "__main__":
    """ 
    This runs only if the program is started from the main.py files
    The result is that it's used only when I test/debug the web page in a local network 
    """
    
    if global_values.INIT_DATABASE:
        from scripts.database_sql import database_initiator
        database_initiator.init_database("local" if global_values.RUN_LOCALLY else "turso")
    
    app.run(host="0.0.0.0", port=8080, debug=True)
        
    