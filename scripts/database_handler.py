import sqlite3

def get_db():
    return sqlite3.connect("routes.db")

def init_db():
    db = get_db()
    db.execute("""
    CREATE TABLE IF NOT EXISTS routes(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        image TEXT,
        holds TEXT
    )
    """)
    db.commit()

def get_routes():
    db = get_db()
    return db.execute("SELECT * FROM routes").fetchall()

def get_route(id):
    db = get_db()
    return db.execute("SELECT * FROM routes WHERE id=?", (id,)).fetchone()

def add_route(image, holds):
    db = get_db()
    db.execute(
        "INSERT INTO routes(image, holds) VALUES (?,?)",
        (image.filename, holds)
    )
    db.commit()