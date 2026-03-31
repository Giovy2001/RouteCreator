import libsql
from datetime import datetime
from scripts.database_sql import sql_holds


### UTILITIES

def format_table(route_object: tuple) -> dict:
    """
    Convert a route tuple into a formatted dictionary with descriptive keys.
    This function takes a tuple containing route information and transforms it
    into a dictionary where each element is mapped to its corresponding field name.
    Args:
        route_object (tuple): A tuple containing route data with 7 elements in the following order:
            - route_id: Unique identifier for the route
            - route_name: Name of the route
            - author: Creator of the route
            - creation_date: Date when the route was created
            - route_grade: Difficulty grade of the route
            - route_description: Description of the route
            - image_url: URL to the route's image
    Returns:
        dict: A dictionary with keys ("route_id", "route_name", "author", "creation_date",
              "route_grade", "route_description", "image_url") mapped to their corresponding
              values from the input tuple.
    """
    
    table_structure: tuple = ("route_id","route_name","author","creation_date","route_grade","route_description","image_url")
    return {table_structure[index]:route_object[index] for index in range(len(table_structure))}

### GETS

def get_all_routes(conn: libsql.Connection) -> list:
    """
    Retrieve all routes from the database.
    Args:
        conn (libsql.Connection): The connection object to the sql database
    Returns:
        routes_list (list): A list of tuples containing all routes from the routes table.
              Each tuple represents a row with all columns from the routes table.
              Returns an empty list if no routes exist.
    """
    
    cursor: libsql.Cursor = conn.cursor()
    routes: list = cursor.execute("SELECT * FROM routes").fetchall()
    return [format_table(route) for route in routes]


def get_routes_from_author(conn: libsql.Connection, author: str) -> list:
    """
    Retrieve all routes from the database that match author.
    Args:
        conn (libsql.Connection): The connection object to the sql database
        author (str): The name of the user.
    Returns:
        routes_list (list): A list of tuples containing all routes from the routes table.
              Each tuple represents a row with all columns from the routes table.
              Returns an empty list if no routes exist.
    """
    
    cursor: libsql.Cursor = conn.cursor()
    routes: list = cursor.execute("SELECT * FROM routes WHERE author=?", (author,)).fetchall()
    return [format_table(route) for route in routes]


def get_route(conn: libsql.Connection, route_id: int) -> dict:
    """
    Retrieve a single route record from the database by its ID.
    Args:
        conn (libsql.Connection): The connection object to the sql database
        route_id (int): The unique identifier of the route to retrieve.
    Returns:
        route (dict): A dictionary containing all columns of the matching route record
    """
    
    cursor: libsql.Cursor = conn.cursor()
    route: tuple = cursor.execute("SELECT * FROM routes WHERE route_id=?", (route_id,)).fetchone()
    return format_table(route)


### SETS

def edit_route(conn: libsql.Connection, route_id: int, data_to_override: dict) -> None:
    """
    Update an existing route in the database with the provided data.
    Args:
        conn (libsql.Connection): The database connection object used to execute the query.
        route_id (int): The unique identifier of the route to be updated.
        data_to_override (dict): A dictionary containing the column names as keys and their new values.
                                 Only the fields specified in this dictionary will be updated.
    """
    
    instruction: str = ", ".join([f'{key} = ?' for key in data_to_override])
    values: list = [data_to_override[key] for key in data_to_override]
    values.append(route_id)

    cursor: libsql.Cursor = conn.cursor()
    cursor.execute(
        f"UPDATE routes SET {instruction} WHERE route_id = ?",
        values
    )
    
    conn.commit()
    

def add_route(conn: libsql.Connection, route_data: dict, holds_data: list) -> None:
    """
    Adds a new climbing route and its associated holds to the database.
    Parameters:
        conn (libsql.Connection): Database connection object used to execute queries.
        route_data (dict): Dictionary containing route data.
        holds_data (list): List containing holds information
    """
    
    creation_date: str = datetime.today().strftime(r'%d-%m-%Y')
    
    cursor: libsql.Cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO routes(route_name, author, creation_date, route_grade, route_description, image_url) VALUES (?,?,?,?,?,?)",
        (route_data["route_name"], route_data["author"], creation_date, route_data["route_grade"], route_data["route_description"], route_data["image_url"])
    )
    
    route_id: int = cursor.lastrowid

    sql_holds.add_holds(conn, route_id, holds_data)
    

### DELETES

def del_route(conn: libsql.Connection, route_id: int) -> None:
    """
    Delete a route and all associated holds from the database.
    Args:
        conn (libsql.Connection): The database connection object used to execute the query.
        route_id (int): The unique identifier of the route to be updated.
    """
    
    sql_holds.del_holds(conn, route_id)
    
    cursor: libsql.Cursor = conn.cursor()
    cursor.execute(
        "DELETE FROM routes WHERE route_id = ?",
        (route_id,)
    )
    
    conn.commit()
    

### INIT

def init_routes_table(conn: libsql.Connection) -> None:
    """
    Initialize the routes table in the database.
    Creates a new table named 'routes' if it does not already exist.
    The table stores information about climbing routes including their
    identifiers, names, authors, creation dates, grades, descriptions,
    and associated image.
    Args:
        conn (libsql.Connection): An active database connection object
            used to execute the CREATE TABLE statement.
    """
    
    cursor: libsql.Cursor = conn.cursor()
    cursor.execute("""CREATE TABLE IF NOT EXISTS routes(
        route_id INTEGER PRIMARY KEY AUTOINCREMENT,
        route_name TEXT,
        author TEXT,
        creation_date TEXT,
        route_grade TEXT,
        route_description TEXT,
        image_url TEXT,
        FOREIGN KEY (author) REFERENCES users(user_name)
    )""")
    
    conn.commit()