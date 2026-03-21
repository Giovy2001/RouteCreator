from scripts.database_sql import sql_init, sql_holds, sql_routes

def init_database(mode: str) -> None:
    """
    Initialize the database by setting up tables based on the specified mode.
    Args:
        mode (str): The database mode to initialize. Supported values are:
            - "turso": Initialize a Turso cloud database connection
            - "local": Initialize a local database connection
    Raises:
        Exception: Raised with message "INFO Database initiated correctly." 
            after successful initialization to indicate completion.
    Note:
        This function initializes the routes and holds tables after establishing
        a database connection. The exception raised at the end is informational
        and indicates successful database setup.
    """
    
    
    match mode:
        case "turso":
            conn = sql_init.init_turso_database()
        case "local":
            conn = sql_init.init_local_database()
        
    sql_routes.init_routes_table(conn)
    sql_holds.init_holds_table(conn)
    
    raise Exception("INFO Database initiated correctly.")