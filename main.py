from flask import Flask
import secrets

app = Flask(__name__)
app.config['SECRET_KEY'] = secrets.token_hex(16)

from scripts import database_handler
from scripts import image_handler
database_handler.init_sql_database()
image_handler.init_glob_database()

from pages import create, index, view

DEBUG = False

if __name__ == "__main__":
    if DEBUG:
        app.run(debug=True)
    else:
        from waitress import serve
        serve(app, host="0.0.0.0", port=8080)