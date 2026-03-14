import os
import libsql

url = os.getenv("TURSO_DATABASE_URL")
token = os.getenv("TURSO_AUTH_TOKEN")
name = "palaenrosadira-routes-sql"

conn = libsql.connect(database=url, auth_token=token)

# Qui aggiungo il nome della via e il grado
conn.execute("""CREATE TABLE IF NOT EXISTS routes(id INTEGER PRIMARY KEY AUTOINCREMENT, image TEXT, holds TEXT)""")
conn.commit()

def get_routes():
    return conn.execute("SELECT * FROM routes").fetchall()

def get_route(id):
    return conn.execute("SELECT * FROM routes WHERE id=?", (id,)).fetchone()

def add_route(image_url, holds):
    conn.execute(
        "INSERT INTO routes(image, holds) VALUES (?,?)",
        (image_url, holds)
    )
    conn.commit()