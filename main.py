from flask import Flask

app = Flask(__name__)

import global_values
global_values.load_database()

if __name__ != "__main__":
    global_values.DEBUG = global_values.RUN_LOCALLY, global_values.RUN_LOCALLY = False

from pages import create, index, view, edit

app.add_url_rule("/",                           view_func=index.index)
app.add_url_rule("/use_condition",              view_func=index.use_condition)

app.add_url_rule("/route_<int:route_id>",       view_func=view.view_route,              methods=["GET", "POST"])
app.add_url_rule("/edit_route_<int:route_id>",  view_func=edit.edit_name_description,   methods=["GET", "POST"])
app.add_url_rule("/edit_holds_<int:route_id>",  view_func=edit.edit_holds,              methods=["GET", "POST"])

app.add_url_rule("/select_image",               view_func=create.select_image,          methods=["GET", "POST"])
app.add_url_rule("/create_route",               view_func=create.create_route,          methods=["GET", "POST"])
app.add_url_rule("/save_route",                 view_func=create.save_route,            methods=["GET", "POST"])


if __name__ == "__main__":
    """ 
    This runs only if the program is started from the main.py files
    The result is that it's used only when I test/debug the web page in a local network 
    """
    
    if global_values.INIT_DATABASE:
        from scripts.database_sql import database_initiator
        database_initiator.init_database("local" if global_values.RUN_LOCALLY else "turso")
    
    if global_values.DEBUG:
        app.run(debug=True)
    else:
        from waitress import serve
        serve(app, host="0.0.0.0", port=8080)