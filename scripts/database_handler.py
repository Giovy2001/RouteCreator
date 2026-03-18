import os
import libsql

def init_sql_database() -> None:
    """
    Initializes the SQL database connection using environment variables.
    This function retrieves the database URL and authentication token from the
    environment variables 'TURSO_DATABASE_URL' and 'TURSO_AUTH_TOKEN', respectively.
    It then establishes a connection to the database using these credentials and
    assigns the connection object to the variable 'conn'.
    Globals:
        url (str): The database URL obtained from the environment variable.
        token (str): The authentication token obtained from the environment variable.
    Raises:
        Any exceptions raised by the underlying database connection library.
    """
    
    global conn
    url = os.getenv("TURSO_DATABASE_URL")
    token = os.getenv("TURSO_AUTH_TOKEN")
    conn = libsql.connect(database=url, auth_token=token)
    
def init_local_database() -> None:
    """
    Initializes the SQL database from local space.
    """
    
    global conn
    conn = libsql.connect("static\\local_database\\sql_database.db")
    

def get_all_routes():
    cursor = conn.cursor()
    return cursor.execute("SELECT * FROM routes").fetchall()

def get_route(id):
    cursor = conn.cursor()
    return cursor.execute("SELECT * FROM routes WHERE id=?", (id,)).fetchone()

def get_holds(id) -> list:
    cursor = conn.cursor()
    holds = cursor.execute("SELECT * FROM holds WHERE route_id = ?", (id,)).fetchall()
    
    holds_list = [{
        "x": h[2] * 1.0,
        "y": h[3] * 1.0,
        "r": h[4],
        "type": h[5],
        "use": h[6]
    } for h in holds]
    
    return holds_list


def add_route(name:str, author:str, image_url:str, description:str, holds:list) -> None:
    cursor = conn.cursor()
    
    """
    Adds a new climbing route and its associated holds to the database.
    Parameters:
        name (str): The name of the route.
        author (str): The author or creator of the route.
        image_url (str): The URL of the image representing the route.
        description (str): A textual description of the route.
        holds (list): A list of dictionaries, each representing a hold with keys:
            - "x" (float or int): The x-coordinate of the hold.
            - "y" (float or int): The y-coordinate of the hold.
            - "size" (str or int): The size of the hold.
            - "type" (str): The type of the hold. start / middle / top
            - "use" (str): The use type of the hold. foot / hand / both
    Returns:
        None
    """

    # Insert the route into the routes table
    cursor.execute(
        "INSERT INTO routes(name, author, image_url, description) VALUES (?,?,?,?)",
        (name, author, image_url, description)
    )
    
    # Get the last autogenerate id
    route_id: int = cursor.lastrowid

    # Insert all the holds associated with the route_id into the holds table
    for hold in holds:
        cursor.execute(
            "INSERT INTO holds (route_id, x, y, size, hold_type, use_type) VALUES (?, ?, ?, ?, ?, ?)", 
            (route_id, hold["x"], hold["y"], hold["scale"], hold["type"], hold["use"])
        )
    
    # Commit the sql changes
    conn.commit()