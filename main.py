from flask import Flask

if __name__ == "__main__":
    from settings import DEBUG, RUN_LOCALLY, INIT_DATABASE
else:
    DEBUG = RUN_LOCALLY = False

app = Flask(__name__)

from scripts import database_handler
from scripts import image_handler

if RUN_LOCALLY:
    database_handler.init_local_database()
    image_handler.init_local_database()
else:
    database_handler.init_sql_database()
    image_handler.init_glob_database()

from pages import create, index, view

app.add_url_rule("/",                       view_func=index.index)
app.add_url_rule("/use_condition",          view_func=index.use_condition)

app.add_url_rule("/route_<int:route_id>",   view_func=view.view_route,      methods=["GET", "POST"])

app.add_url_rule("/select_image",           view_func=create.select_image,  methods=["GET", "POST"])
app.add_url_rule("/create_route",           view_func=create.create_route,  methods=["GET", "POST"])
app.add_url_rule("/save_route",             view_func=create.save_route,    methods=["GET", "POST"])

if __name__ == "__main__":
    """ 
    This runs only if the program is started from the main.py files
    The result is that it's used only when I test/debug the web page in a local network 
    """
    
    if INIT_DATABASE:
        from scripts import database_initiator
        database_initiator.init_database("local" if RUN_LOCALLY else "turso")
        raise Exception("INFO Database initiated correctly.")
    
    if DEBUG:
        app.run(debug=True)
    else:
        from waitress import serve
        serve(app, host="0.0.0.0", port=8080)