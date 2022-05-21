import sqlite3


class User:

    def __init__(self, table_name='users', file_name='db.sql'):
        self.table = table_name
        self.file = file_name
        self.conn = ''
        self.cur = ''
        self.create_table()

    def connect(self):
        self.conn = sqlite3.connect(self.file)
        self.cur = self.conn.cursor()

    def create_table(self):
        self.connect()
        self.cur.execute('''CREATE TABLE IF NOT EXISTS {} (
            userid INTEGER PRIMARY KEY,
            firstname TEXT NOT NULL,
            lastname TEXT NOT NULL,
            age INTEGER NOT NULL,
            password TEXT NOT NULL,
            email TEXT NOT NULL);
        '''.format(self.table))
        self.conn.commit()
        self.conn.close()

    def create_user(self, user_info):
        self.connect()
        self.cur.execute(
            "INSERT INTO {} (firstname, lastname, age, password, email) VALUES(?, ?, ?, ?, ?)".format(self.table),
            user_info)
        self.conn.commit()
        result = self.cur.execute("SELECT MAX(userid) FROM {};".format(self.table)).fetchone()[0]
        self.conn.close()
        return result

    def get(self, user_id):
        self.connect()
        result = self.cur.execute("SELECT * FROM {} WHERE userid = {}".format(self.table, user_id)).fetchone()
        self.conn.close()
        return result

    def all(self):
        self.connect()
        result = self.cur.execute("SELECT * FROM {};".format(self.table)).fetchall()
        self.conn.close()
        return result

    def update(self, user_id, attribute, value):
        self.connect()
        self.cur.execute("UPDATE {} SET {} = '{}' WHERE userid = {}".format(self.table, attribute, value, user_id))
        self.conn.commit()
        result = self.cur.execute("SELECT * FROM {} WHERE userid = {}".format(self.table, user_id)).fetchone()
        self.conn.close()
        return result

    def destroy(self, user_id):
        self.connect()
        self.cur.execute("DELETE FROM {} WHERE userid = {}".format(self.table, user_id))
        self.conn.commit()
        self.conn.close()

