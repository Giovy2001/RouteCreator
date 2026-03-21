from scripts.database_sql import sql_init
from scripts import image_handler

DEBUG: bool = False
RUN_LOCALLY: bool = True
INIT_DATABASE: bool = False

# Initialize database

def load_database() -> None:
    global conn
    if RUN_LOCALLY:
        conn = sql_init.init_local_database()
        image_handler.init_local_database()
    else:
        conn = sql_init.init_sql_database()
        image_handler.init_glob_database()