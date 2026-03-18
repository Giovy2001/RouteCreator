def init_database(mode: str) -> None:
    """
    Init the database by creating the right structure.

    Args:
        mode (str): local / turso
    """
    
    import os
    import libsql

    if mode == "local":
        conn = libsql.connect("static\\local_database\\sql_database.db")
    else:
        url = os.getenv("TURSO_DATABASE_URL")
        token = os.getenv("TURSO_AUTH_TOKEN")
        conn = libsql.connect(database=url, auth_token=token)

    conn.execute("""CREATE TABLE IF NOT EXISTS routes(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        author TEXT,
        image_url TEXT,
        description TEXT
    )""")
    conn.execute("""CREATE TABLE IF NOT EXISTS holds(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        route_id INTEGER,
        x REAL,
        y REAL,
        size REAL,
        hold_type TEXT,
        use_type TEXT,
        FOREIGN KEY (route_id) REFERENCES routes(id)
    );""")
    conn.commit()