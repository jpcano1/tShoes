import psycopg2
import datetime
import os

class Authtoken:
    """ Class that allows me to handle token storage """

    # Host
    POSTGRES_HOST = os.environ.get("DB_HOST")

    # Port
    POSTGRES_PORT = os.environ.get("DB_PORT")

    # User
    POSTGRES_USER = os.environ.get("POSTGRES_USER")

    # Password
    POSTGRES_PASSWORD = os.environ.get("POSTGRES_PASSWORD")

    # Database
    POSTGRES_DB = os.environ.get("POSTGRES_DB")

    def __init__(self, **kwargs):
        """
            Constructor class
            :param kwargs: Keyword Arguments
        """
        self.host = self.POSTGRES_HOST
        self.port = self.POSTGRES_PORT
        self.user = self.POSTGRES_USER
        self.passwd = self.POSTGRES_PASSWORD
        self.db = self.POSTGRES_DB
        self.conn = psycopg2.connect(dbname = self.db,
                                     host=self.host,
                                     port=self.port,
                                     user=self.user,
                                     password = self.passwd)
        self.cursor = self.conn.cursor()


    def fetch_user_by_email(self, email):
        """
            Retrieves user from email
            :param email:
            :return: The email of the user
        """
        self.cursor.execute(f"SELECT id FROM users_user WHERE email='{email}'")
        row = self.cursor.fetchone()
        id = row[0]
        return id

    def fetch_users(self):
        """
            Retrieves al users in Database
            :return: An array of tuples
        """
        self.cursor.execute("SELECT * FROM users_user")
        rows = self.cursor.fetchall()
        return rows

    def fetch_authtokens(self):
        """
            Retrieves all authtokens in Database
            :return: An array of tuples
        """
        self.cursor.execute("SELECT * FROM authtoken_token")
        rows = self.cursor.fetchall()
        return rows

    def insert_authtoken(self, user_id, token):
        """
            Creates token in database
            :param user_id: The id of the user asociated to the token
            :param token: The token asociated to the user_id
        """
        date = datetime.datetime.now()
        self.cursor.execute(f"INSERT INTO authtoken_token (key, created, user_id) VALUES ('{token}', TIMESTAMP WITH TIME ZONE '{date}', '{user_id}')")
        self.conn.commit()

    def delete_authtoken(self, user_id):
        """
            Deletes the token after the user logs out
         """
        self.cursor.execute(f"DELETE FROM authtoken_token WHERE user_id = '{user_id}'")
        self.conn.commit()
