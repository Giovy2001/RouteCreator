import libsql


### UTILITIES

def format_table(hold_object: tuple) -> dict:
    """
    Convert a hold tuple into a formatted dictionary with descriptive keys.
    This function takes a tuple containing hold information and transforms it
    into a dictionary where each element is mapped to its corresponding field name.
    Args:
        hold_object (tuple): A tuple containing hold data with 7 elements in the following order:
            - hold_id (int):
            - route_id (int):
            - x (float):
            - y (float):
            - size (float):
            - progression_id (str):
            - constraint_id (str):
    Returns:
        dict
    """
    
    table_structure: tuple = ("hold_id","route_id","x","y","size","progression_id","constraint_id")
    return {table_structure[index]:hold_object[index] for index in range(len(table_structure))}


### GETS

def get_holds(conn: libsql.Connection, route_id: int) -> list:
    """
    Retrieve all holds associated with a specific route.
    Args:
        conn (libsql.Connection): An active database connection object
        id: The route ID to fetch holds for.
    Returns:
        list: A list of dictionaries, each containing hold information
    """
    
    cursor: libsql.Cursor = conn.cursor()
    holds = cursor.execute("SELECT * FROM holds WHERE route_id = ?", (route_id,)).fetchall()
    
    return [format_table(hold) for hold in holds]


### SETS

def add_holds(conn: libsql.Connection, route_id: int, holds_data: list) -> None:
    """
    Insert multiple climbing holds into the database for a specific route.
    Args:
        conn (libsql.Connection): Database connection object used to execute queries.
        route_id (int): The unique identifier of the route to which holds are being added.
        holds_data (list): A list of dictionaries containing hold information. Each dictionary
                          should have the following keys:
                          - x (float): The x-coordinate of the hold.
                          - y (float): The y-coordinate of the hold.
                          - size (str): The size classification of the hold.
                          - progression (int): The progression ID associated with the hold.
                          - constraint (int): The constraint ID associated with the hold.
    """
    
    cursor: libsql.Cursor = conn.cursor()
    for hold in holds_data:
        cursor.execute(
            "INSERT INTO holds (route_id, x, y, size, progression_id, constraint_id) VALUES (?, ?, ?, ?, ?, ?)", 
            (route_id, hold["x"], hold["y"], hold["size"], hold["progression_id"], hold["constraint_id"])
        )
        
    conn.commit()


def edit_holds(conn: libsql.Connection, route_id:int, holds_data: list) -> None:
    """
    Update the holds associated with a route in the database.
    This function deletes all existing holds for a given route and inserts
    new holds based on the provided list. Changes are committed to the database.
    Args:
        conn (libsql.Connection): Database connection object used to execute queries.
        route_id (int): The unique identifier of the route whose holds will be updated.
        holds_data (list): A list of dictionaries, each containing hold information.
    """
    
    cursor: libsql.Cursor = conn.cursor()
    cursor.execute(
        "DELETE FROM holds WHERE route_id = ?",
        (route_id,)
    )
    conn.commit()
    
    add_holds(conn, route_id, holds_data)
    

### DELETES

def del_holds(conn: libsql.Connection, route_id: int) -> None:
    """
    Delete all holds associated with route_id from the database.
    Args:
        conn (libsql.Connection): The database connection object used to execute the query.
        route_id (int): The unique identifier of the route to be updated.
    """
    
    cursor: libsql.Cursor = conn.cursor()
    cursor.execute(
        "DELETE FROM holds WHERE route_id = ?",
        (route_id,)
    )
    conn.commit()
  
    
### INIT
    
def init_holds_table(conn: libsql.Connection) -> None:
    """
    Initialize the holds table in the database.
    Creates a new table named 'holds' if it does not already exist.
    The table stores information about holds in the climbing route including their
    identifiers, position, size, and types.
    - progression_id: [start, middle, zone, top]
    - constraint_id: [normal, foot, only_hand, only_foot, only_volume, no_volume]
    Args:
        conn (libsql.Connection): An active database connection object
            used to execute the CREATE TABLE statement.
    """
    
    cursor: libsql.Cursor = conn.cursor()
    cursor.execute("""CREATE TABLE IF NOT EXISTS holds(
        hold_id INTEGER PRIMARY KEY AUTOINCREMENT,
        route_id INTEGER,
        x REAL,
        y REAL,
        size REAL,
        progression_id TEXT,
        constraint_id TEXT,
        FOREIGN KEY (route_id) REFERENCES routes(route_id)
    );""")
    
    conn.commit()
    
