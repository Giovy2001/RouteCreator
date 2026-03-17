from flask import Flask
import secrets

app = Flask(__name__)
app.config['SECRET_KEY'] = secrets.token_hex(16)

from scripts import database_handler
from scripts import image_handler
database_handler.init_sql_database()
image_handler.init_glob_database()

from pages import create, index, view

app.add_url_rule("/", view_func=index.index)
app.add_url_rule("/route/<int:route_id>", view_func=view.view_route)
app.add_url_rule("/select_image", view_func=create.select_image, methods=["GET", "POST"])
app.add_url_rule("/create_route", view_func=create.create_route, methods=["GET", "POST"])
app.add_url_rule("/save_route", view_func=create.save_route, methods=["GET", "POST"])

if __name__ == "__main__":
    """ 
    This runs only if the program is started from the main.py files
    The result is that it's used only when I test/debug the web page in a local network 
    """
    
    DEBUG: bool = False
    
    if DEBUG:
        app.run(debug=True)
    else:
        from waitress import serve
        serve(app, host="0.0.0.0", port=8080)
        
    