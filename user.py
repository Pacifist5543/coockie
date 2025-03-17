import sqlite3
import hashlib

db_name = "data.db"

def create_user_table():
    SQL = """
    CREATE TABLE IF NOT EXISTS user (
        id integer primary key,
        username text unique,
        password_hash text)"""
    
    con = sqlite3.connect(db_name)
    con.execute(SQL)

class User:
    def __init__(self, username, id, password_hash):
        self.username = username
        self.id = id
        self.password_hash = password_hash


    @staticmethod
    def get_users_by_username(username):
        SQL = "SELECT * FROM user where username = ?"
        con = sqlite3.connect(db_name)
        q = con.execute(SQL, [username])
        data = q.fetchone()
        if not data:
            return None
        return User(*data)
    
    @staticmethod
    def hashed_password(password):
        return hashlib.sha256(password.encode()).hexdigest()

    
    @staticmethod
    def creat(username, password):
        password_hash = User.hashed_password(password)

        SQL = """
            insert into user(username, password_hash)
            values (?, ?)
            """ 
        con = sqlite3.connect(db_name)
        con.execute(SQL, [username, password_hash])
        con.commit()
        
