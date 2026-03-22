import libsql


### UTILITIES

def format_table(beta_object: tuple) -> dict:
    """
    Convert a beta tuple into a formatted dictionary with structured keys.
    This function takes a tuple containing beta information and maps it to a dictionary
    using predefined column names as keys.
    Args:
        beta_object (tuple): A tuple containing beta data in the order of
            (beta_id, route_id, title, body).
    Returns:
        dict: A dictionary with keys ('beta_id', 'route_id', 'title', 'body')
            mapped to their corresponding values from the input tuple.
    """
    
    table_structure: tuple = ("beta_id","route_id","title","body")
    return {table_structure[index]:beta_object[index] for index in range(len(table_structure))}


### GETS

def get_betas(conn: libsql.Connection, route_id: int) -> list:
    """
    Retrieve all betas associated with a specific route.
    Args:
        conn (libsql.Connection): An active database connection object
        route_id: The route ID to fetch betas for.
    Returns:
        list: A list of dictionaries, each containing betas information
    """
    
    cursor: libsql.Cursor = conn.cursor()
    betas = cursor.execute("SELECT * FROM betas WHERE route_id = ?", (route_id,)).fetchall()
    
    return [format_table(beta) for beta in betas]


### SETS

def add_beta(conn: libsql.Connection, route_id: int, beta_data: list) -> None:
    """
    Insert a new beta entry into the database.
    Args:
        conn (libsql.Connection): Database connection object.
        route_id (int): The ID of the route associated with the beta.
        beta_data (list): A dictionary containing beta information with keys:
            - title (str): The title of the beta.
            - body (str): The body/content of the beta.
    """
    
    cursor: libsql.Cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO betas (route_id, title, body) VALUES (?, ?, ?)", 
        (route_id, beta_data["title"], beta_data["body"])
    )
        
    conn.commit()


def edit_beta(conn: libsql.Connection, beta_id:int, data_to_override: dict) -> None:
    """
    Update an existing route in the database with the provided data.
    Args:
        conn (libsql.Connection): The database connection object used to execute the query.
        beta_id (int): The unique identifier of the beta to be updated.
        data_to_override (dict): A dictionary containing the column names as keys and their new values.
                                 Only the fields specified in this dictionary will be updated.
    """
    
    instruction: str = ", ".join([f'{key} = ?' for key in data_to_override])
    values: list = [data_to_override[key] for key in data_to_override]
    values.append(beta_id)

    cursor: libsql.Cursor = conn.cursor()
    cursor.execute(
        f"UPDATE routes SET {instruction} WHERE beta_id = ?",
        values
    )
    
    conn.commit()
    

### DELETES

def del_beta(conn: libsql.Connection, beta_id: int) -> None:
    """
    Delete beta with beta_id from the database.
    Args:
        conn (libsql.Connection): The database connection object used to execute the query.
        beta_id (int): The unique identifier of the beta.
    """
    
    cursor: libsql.Cursor = conn.cursor()
    cursor.execute(
        "DELETE FROM betas WHERE beta_id = ?",
        (beta_id,)
    )
    conn.commit()
    
    
def del_betas(conn: libsql.Connection, route_id: int) -> None:
    """
    Delete all betas associated with route_id from the database.
    Args:
        conn (libsql.Connection): The database connection object used to execute the query.
        route_id (int): The unique identifier of the route.
    """
    
    cursor: libsql.Cursor = conn.cursor()
    cursor.execute(
        "DELETE FROM betas WHERE route_id = ?",
        (route_id,)
    )
    conn.commit()
  
    
### INIT
    
def init_betas_table(conn: libsql.Connection) -> None:
    """
    Initialize the betas table in the database.
    Creates a new table named 'betas' if it does not already exist.
    The table stores beta information (climbing route guides/tips).
    Args:
        conn (libsql.Connection): Database connection object used to execute
                                  the CREATE TABLE statement and commit changes.
    """
    
    cursor: libsql.Cursor = conn.cursor()
    cursor.execute("""CREATE TABLE IF NOT EXISTS betas(
        beta_id INTEGER PRIMARY KEY AUTOINCREMENT,
        route_id INTEGER,
        title TEXT,
        body TEXT,
        FOREIGN KEY (route_id) REFERENCES routes(route_id)
    );""")
    
    conn.commit()
    
