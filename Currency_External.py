import sqlite3
import os

dir_path = os.path.dirname(os.path.realpath("main.py")) + "/databases/"


def fetch_server_database(guild_id):
    # Searches through list of dir for database file with name of server_id
    # returns a sqlite3 connection object

    databases = os.listdir(dir_path)
    database_name = "accounts_" + str(guild_id) + ".db"
    if database_name in databases:
        conn = sqlite3.connect(dir_path + database_name)
        return conn
    else:
        conn = sqlite3.connect(dir_path + database_name)
        c = conn.cursor()
        c.execute("""CREATE TABLE guild_accounts (
                    guild_id text,
                    member_id text,
                    m_balance text,
                    g_balance text,
                    b_balance text,
                    steal_risk text,
                    knife text,
                    knife_bonus text
                )""")
        conn.commit()
        return conn


class Account:

    def __init__(self, guild_id, member_id, m_balance, g_balance, b_balance, steal_risk, knife, knife_bonus):
        self.guild_id = int(guild_id)
        self.member_id = int(member_id)
        self.m_balance = int(m_balance)
        self.g_balance = int(g_balance)
        self.b_balance = (b_balance)
        self.steal_risk = int(steal_risk)
        self.knife = knife
        self.knife_bonus = int(knife_bonus)

    def add_m_balance(self, num):
        database = fetch_server_database(self.guild_id)
        c = database.cursor()

        new_m_balance = self.m_balance + num

        new_m_balance = str(new_m_balance)
        self.m_balance = int(new_m_balance)
        with database:
            c.execute("""UPDATE guild_accounts SET m_balance = :bal
                        WHERE guild_id = :g_id AND member_id = :m_id""",
                      {'bal': new_m_balance, 'g_id': self.guild_id, 'm_id': self.member_id})

    def add_g_balance(self, num):
        database = fetch_server_database(self.guild_id)
        c = database.cursor()

        new_g_balance = self.g_balance + num

        new_g_balance = str(new_g_balance)
        self.g_balance = int(new_g_balance)
        with database:
            c.execute("""UPDATE guild_accounts SET g_balance = :bal
                        WHERE guild_id = :g_id AND member_id = :m_id""",
                      {'bal': new_g_balance, 'g_id': self.guild_id, 'm_id': self.member_id})

    def add_b_balance(self, num):
        database = fetch_server_database(self.guild_id)
        c = database.cursor()

        new_b_balance = self.b_balance + num

        new_b_balance = str(new_b_balance)
        self.b_balance = int(new_b_balance)
        with database:
            c.execute("""UPDATE guild_accounts SET b_balance = :bal
                        WHERE guild_id = :g_id AND member_id = :m_id""",
                      {'bal': new_b_balance, 'g_id': self.guild_id, 'm_id': self.member_id})


def fetch_account(guild_id, member_id):
    guild_id = str(guild_id)
    member_id = str(member_id)

    database = fetch_server_database(guild_id)
    c = database.cursor()
    c.execute("SELECT * FROM guild_accounts WHERE member_id=:id", {'id': member_id})
    info = c.fetchone()
    if info is not None:
        pass
    else:
        c.execute("INSERT INTO guild_accounts VALUES (:g_id, :m_id, '0', '0', '0', '0', 'Rusty Knife', '20')",
                  {'g_id': guild_id, 'm_id': member_id})
        database.commit()
        c.execute("SELECT * FROM guild_accounts WHERE member_id=:id", {'id': member_id})
        info = c.fetchone()
    return Account(info[0], info[1], info[2], info[3], info[4], info[5], info[6], info[7])


def fetch_all_accounts(guild_id):
    guild_id = str(guild_id)
    conn = fetch_server_database(guild_id)
    c = conn.cursor()
    c.execute("SELECT * FROM guild_accounts")
    rows = c.fetchall()
    list_of_accounts = []
    for info in rows:
        list_of_accounts.append(Account(info[0], info[1], info[2], info[3], info[4], info[5], info[6], info[7]))
    return list_of_accounts


def update_databases():
    databases = os.listdir(dir_path)
    for i in databases:
        if str(i) not in ["sniper.db"]:
            conn = sqlite3.connect(dir_path + i)
            c = conn.cursor()
            c.execute("""CREATE TABLE guild_bank_accounts (
                                        guild_id text,
                                        member_id text,
                                        balance text,
                                        account_tier text,
                                        interest text
                                    )""")
            conn.commit()
