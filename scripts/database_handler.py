import os
import libsql
from datetime import datetime

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
    """
    Retrieve all routes from the database.
    Returns:
        list: A list of tuples containing all routes from the routes table.
              Each tuple represents a row with all columns from the routes table.
              Returns an empty list if no routes exist.
    Raises:
        DatabaseError: If there is an error executing the query or connecting to the database.
    """
    
    cursor = conn.cursor()
    return cursor.execute("SELECT * FROM routes").fetchall()

def get_route(id):
    """
    Retrieve a single route record from the database by its ID.
    Args:
        id: The unique identifier of the route to retrieve.
    Returns:
        tuple or None: A tuple containing all columns of the matching route record,
                       or None if no route with the given ID exists.
    Raises:
        DatabaseError: If there is an error executing the database query.
    """
    
    cursor = conn.cursor()
    return cursor.execute("SELECT * FROM routes WHERE id=?", (id,)).fetchone()

def get_holds(id: int) -> list:
    """
    Retrieve all holds associated with a specific route.
    Args:
        id: The route ID to fetch holds for.
    Returns:
        list: A list of dictionaries, each containing hold information with keys:
            - x (float): The x-coordinate of the hold.
            - y (float): The y-coordinate of the hold.
            - r (str): The radius or size property of the hold.
            - type (str): The type of the hold.
            - use (str): The usage or classification of the hold.
    """
    
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

def del_route(image_url: str) -> None:
    """
    Delete a route and all associated holds from the database.
    This function removes a route record and its related holds entries
    from the database based on the provided image URL.
    Args:
        image_url (str): The image URL of the route to delete.
    Raises:
        TypeError: If the image_url is not found in the database (fetchone() returns None).
    Returns:
        None
    """
    
    cursor = conn.cursor()
    route_id: int = cursor.execute("SELECT * FROM routes WHERE image_url = ?", (image_url,)).fetchone()[0]
    cursor.execute(
        "DELETE FROM holds WHERE route_id = ?",
        (route_id,)
    )    
    cursor.execute(
        "DELETE FROM routes WHERE id = ?",
        (route_id,)
    )
    conn.commit()

def add_route(name:str, author:str, image_url:str, description:str, holds:list) -> None:
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
    cursor = conn.cursor()

    # Insert the route into the routes table
    formatted_today = datetime.today().strftime(r'%d-%m-%Y')
    cursor.execute(
        "INSERT INTO routes(name, author, image_url, description, date) VALUES (?,?,?,?,?)",
        (name, author, image_url, description, formatted_today)
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
    
def edit_name_description(id:int, name:str, description:str) -> None:
    """
    Update the name and description of a route in the database.
    Args:
        id (int): The unique identifier of the route to update.
        name (str): The new name for the route.
        description (str): The new description for the route.
    Returns:
        None
    Raises:
        sqlite3.Error: If the database operation fails.
    """

    cursor = conn.cursor()
    
    cursor.execute(
        "UPDATE routes SET name = ?, description = ? WHERE id = ?",
        (name, description, id)
    )
    
    # Commit the sql changes
    conn.commit()