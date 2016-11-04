import sys
import psycopg2
import psycopg2.extras


class Database:

    def __init__(self):
        try:
            self.conn = psycopg2.connect(database='d3eqp4tbb873a3', user='wddgtmcjcukqte', port=5432, password='uLOXVJ2K1bnlGv8B7hG6y7mrF6')
            self.cursor = self.conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        except psycopg2.DatabaseError as err:
            print('Error {}'.format(err))
            sys.exit(1)

    @property
    def version(self):
        return self.cursor.execute('SELECT version()')

    def teardown(self):
        self.conn.close()

    def add_user(self, username, password):
        # Look for username - apparently psycopg2 protects agains sql injection
        self.cursor.execute("SELECT * FROM Users WHERE Username=%s", username)
        users = self.cursor.fetchall()
        if users:
            return (409, 'Username already exists')
        self.cursor.execute(
            "INSERT INTO Users VALUES (%s,%s,%s)",
            (username, password)
        )
        return (None, None)  # all OK

    def user_auth(self, username, password):
        self.cursor.execute("SELECT * FROM Users WHERE Username=%s", username)
        user = self.cursor.fetchall()
        if not user:
            return False
        return user['password'] == password

    def add_pool(self, pool, username, names):
        pass
