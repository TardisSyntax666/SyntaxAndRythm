import sqlite3
import os

dir_path = os.path.dirname(os.path.realpath("main.py")) + "/databases/"


def fetch_server_database():
    # Searches through list of dir for database file with name of server_id
    # returns a sqlite3 connection object

    databases = os.listdir(dir_path)
    database_name = f"messages_.db"
    if database_name in databases:
        conn = sqlite3.connect(dir_path + database_name)
        return conn
    else:
        conn = sqlite3.connect(dir_path + database_name)
        c = conn.cursor()
        c.execute("""CREATE TABLE messages_edit (
                    channel_id text,
                    message_id,
                    member_id text,
                    content text,
                    time text
                )""")
        conn.commit()
        c.execute("""CREATE TABLE messages_delete (
                            channel_id text,
                            member_id text,
                            content text,
                            time text
                        )""")
        conn.commit()
        return conn


def set_d_message(guild_id, channel_id, member_id, content, time):
    database = fetch_server_database()
    c = database.cursor()
    c.execute("INSERT INTO messages_delete VALUES (:c_id, :m_id, :c, :t)",
              {'c_id': channel_id, 'm_id': member_id, "c": content, "t": time})
    database.commit()


def set_e_message(channel_id, message_id, member_id, content, time):
    database = fetch_server_database()
    c = database.cursor()
    c.execute("INSERT INTO messages_edit VALUES (:c_id, :me_id, :m_id, :c, :t)",
              {'c_id': channel_id, 'me_id': message_id, 'm_id': member_id, "c": content, "t": time})
    database.commit()


def fetch_d_message(channel_id):
    channel_id = str(channel_id)

    database = fetch_server_database()
    c = database.cursor()
    c.execute("SELECT * FROM messages_delete WHERE channel_id=:id", {'id': channel_id})
    info = c.fetchone()
    if info is not None:
        return {"channel_id": info[0], "member_id": info[1], "content": info[2], "time": info[3]}
    else:
        return None


def fetch_e_message(message_id):
    message_id = str(message_id)

    database = fetch_server_database()
    c = database.cursor()
    c.execute("SELECT * FROM messages_edit WHERE message_id=:id", {'id': message_id})
    info = c.fetchone()
    if info is not None:
        return {"channel_id": info[0], "message_id": info[1], "member_id": info[2], "content": info[3], "time": info[4]}
    else:
        return None
