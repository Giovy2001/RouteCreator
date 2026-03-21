import os, libsql

def init_turso_database() -> libsql.Connection:
    """
    Initializes the SQL database connection using environment variables.
    This function retrieves the database URL and authentication token from the
    environment variables 'TURSO_DATABASE_URL' and 'TURSO_AUTH_TOKEN', respectively.
    It then establishes a connection to the database using these credentials and
    assigns the connection object to the variable 'conn'.
    Globals:
        url (str): The database URL obtained from the environment variable.
        token (str): The authentication token obtained from the environment variable.
    Returns:
        conn (libsql.Connection): The connection object to the sql database
    """
    
    url = os.getenv("TURSO_DATABASE_URL")
    token = os.getenv("TURSO_AUTH_TOKEN")
    return libsql.connect(database=url, auth_token=token)
    
def init_local_database() -> libsql.Connection:
    """
    Initializes the SQL database from local space.
    Returns:
        conn (libsql.Connection): The connection object to the sql database
    """
    
    return libsql.connect("static\\local_database\\sql_database.db")