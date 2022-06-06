import sqlite3
import os

dir_path = os.path.dirname(os.path.realpath("main.py")) + "/databases/"


def fetch_category_database(id):
    # Searches through list of dir for database file with name of server_id
    # returns a sqlite3 connection object

    databases = os.listdir(dir_path)
    database_name = f"channel_points_{id}.db"
    if database_name in databases:
        conn = sqlite3.connect(dir_path + database_name)
        return conn
    else:
        conn = sqlite3.connect(dir_path + database_name)
        c = conn.cursor()
        c.execute("""CREATE TABLE channels (
                    channel_id text,
                    points text
                )""")
        conn.commit()
        return conn


def set_channel_points(category_id, channel_id, points):
    database = fetch_category_database(category_id)
    c = database.cursor()
    c.execute("SELECT * FROM channels WHERE channel_id=:id", {'id': channel_id})
    info = c.fetchone()
    if info is not None:
        c.execute("UPDATE channels SET points=:p WHERE channel_id=:id", {'p': points, 'id': channel_id})
        database.commit()
    else:
        c.execute("INSERT INTO channels VALUES (:c_id, :p)",
                  {'c_id': channel_id, 'p': points})
        database.commit()



def get_channel_points(category_id, channel_id):
    database = fetch_category_database(category_id)
    c = database.cursor()
    c.execute("SELECT * FROM channels WHERE channel_id=:id", {'id': channel_id})
    info = c.fetchone()
    if info is not None:
        return info[1]
    else:
        set_channel_points(category_id, channel_id, str(0))
        return 0
