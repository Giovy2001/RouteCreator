import libsql
from datetime import datetime
from scripts.database_sql import sql_holds
import json

### UTILITIES

def format_table(user_object: tuple) -> dict:
    """
    Convert a user tuple from the database into a formatted dictionary.
    This function maps a tuple of user data to a dictionary with descriptive keys,
    and deserializes the completed routes from JSON format.
    Args:
        user_object (tuple): A tuple containing user data in the following order:
            - user_id: Unique identifier for the user
            - user_name: Name of the user
            - user_icon: Icon associated with the user
            - user_color: Color preference of the user
            - creation_date: Date when the user account was created
            - last_seen_date: Date when the user was last active
            - points: User's accumulated points
            - serialized_completed_routes: JSON string of completed routes (deserialized as a list)
    """
    
    table_structure: tuple = ("user_id", "user_name", "user_icon", "user_color", "creation_date", "last_seen_date", "points", "serialized_completed_routes")
    user_dict: dict = {table_structure[index]:user_object[index] for index in range(len(table_structure))}
    user_dict["serialized_completed_routes"] = json.loads(user_dict["serialized_completed_routes"])
    return user_dict


### GETS

def get_all_users(conn: libsql.Connection) -> list:
    """
    Retrieve all users from the database.
    Args:
        conn (libsql.Connection): A database connection object to execute queries.
    Returns:
        list: A list of formatted user records from the users table. Each user is 
              formatted using the format_table function.
    """
    
    cursor: libsql.Cursor = conn.cursor()
    users: list = cursor.execute("SELECT * FROM users").fetchall()
    return [format_table(user) for user in users]


def get_user(conn: libsql.Connection, user_name: int) -> dict:
    """
    Retrieve a user from the database by username.
    Args:
        conn (libsql.Connection): Database connection object.
        user_name (str): The username to search for in the users table.
    Returns:
        dict: A formatted dictionary containing the user's information.
    """
    
    cursor: libsql.Cursor = conn.cursor()
    user: tuple = cursor.execute("SELECT * FROM users WHERE user_name=?", (user_name,)).fetchone()
    return format_table(user)


### SETS

def edit_user(conn: libsql.Connection, user_name: int, data_to_override: dict) -> None:
    """
    Update user information in the database.
    Args:
        conn (libsql.Connection): The database connection object.
        user_name (str): The username to search for in the users table.
        data_to_override (dict): A dictionary containing the column names as keys 
                                 and their new values to update in the users table.
    """
    
    instruction: str = ", ".join([f'{key} = ?' for key in data_to_override])
    values: list = [data_to_override[key] for key in data_to_override]
    values.append(user_name)

    cursor: libsql.Cursor = conn.cursor()
    cursor.execute(
        f"UPDATE users SET {instruction} WHERE user_name = ?",
        values
    )
    
    conn.commit()
    

def edit_completed_routes(conn: libsql.Connection, user_name: int, completed_routes: list) -> None:
    """
    Update the completed routes for a user in the database.
    Args:
        conn (libsql.Connection): The database connection object.
        user_name (str): The username to search for in the users table.
        completed_routes (list): A list of completed routes to be associated with the user.
    Notes:
        - The completed routes list is serialized to JSON before being stored in the database.
    """
    
    serialized_completed_routes: str = json.dumps(completed_routes)
    
    cursor: libsql.Cursor = conn.cursor()
    cursor.execute(
        f"UPDATE users SET serialized_completed_routes = ? WHERE user_name = ?",
        (serialized_completed_routes, user_name)
    )
    
    conn.commit()


def add_user(conn: libsql.Connection, user_data: dict) -> None:
    """
    Add a new user to the database.
    Args:
        conn (libsql.Connection): Database connection object used to execute queries.
        user_data (dict): Dictionary containing user information with the following keys:
            - user_name (str): The username of the new user.
            - user_icon (str): The icon/avatar identifier for the user.
            - user_color (str): The color preference for the user.
    Notes:
        - The creation_date and last_seen_date are automatically set to the current date.
        - Initial points are set to 0.
        - serialized_completed_routes is initialized as an empty JSON array.
    """
    
    creation_date: str = datetime.today().strftime(r'%d-%m-%Y')
    
    cursor: libsql.Cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO users(user_name, user_icon, user_color, creation_date, last_seen_date, points, serialized_completed_routes) VALUES (?,?,?,?,?,?,?)",
        (user_data["user_name"], user_data["user_icon"], user_data["user_color"], creation_date, creation_date, 0, json.dumps([]))
    )
    
    conn.commit()
    

### DELETES

def del_user(conn: libsql.Connection, user_name: int) -> None:
    """
    Delete a user from the database by their user ID.
    Args:
        conn (libsql.Connection): The database connection object used to execute the query.
        user_name (str): The username to search for in the users table.
    """
    
    cursor: libsql.Cursor = conn.cursor()
    cursor.execute(
        "DELETE FROM users WHERE user_name = ?",
        (user_name,)
    )
    
    conn.commit()
    

### INIT

def init_users_table(conn: libsql.Connection) -> None:
    """
    Initialize the users table in the database.
    Creates a new 'users' table if it does not already exist. The table stores
    user profile information including identification, preferences, activity tracking,
    and progress metrics.
    Args:
        conn (libsql.Connection): A LibSQL database connection object used to execute
                                   the CREATE TABLE statement and commit changes.
    """

    cursor: libsql.Cursor = conn.cursor()    
    cursor.execute("""CREATE TABLE IF NOT EXISTS users(
        user_id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_name TEXT,
        user_icon TEXT,
        user_color TEXT,
        creation_date TEXT,
        last_seen_date TEXT,
        points INTEGER,
        serialized_completed_routes TEXT
    )""")
    
    conn.commit()