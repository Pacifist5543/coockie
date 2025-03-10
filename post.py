import sqlite3
import hashlib
import datetime

db_name = "data.db"


def create_post_table():
    SQL = """
    CREATE TABLE IF NOT EXISTS post (
        id integer primary key,
        title text,
        description text,
        at_publish text,
        author_id integer 
        )"""

    con = sqlite3.connect(db_name)
    con.execute(SQL)


class Post:
    def __init__(self, id, title, deacription, at_publish, athor_id):
        self.id = id
        self.title = title
        self.deacription = deacription
        self.at_publish = at_publish
        self.athor_id = athor_id

    @staticmethod
    def create(title, description, author_id):
        at_publish = datetime.datetime.now().strftime("%d.%m.%Y %H:%M")

        sql = """
            insert into post(title, description, at_publish, author_id)
            where (?, ?, ?, ?)
        """
        con = sqlite3.connect(db_name)
        con.execute(sql, [title, description, at_publish, author_id])
        con.commit()

    @staticmethod
    def get_post_by_author_id(author_id):
        sql = """
            select * from post where author_id = ?
            """
        con = sqlite3.connect(db_name)
        q = con.execute(sql, [author_id])
        data = q.fetchall()
        return [Post(*row) for row in data]

    @staticmethod
    def get_all():
        sql = """
            select * from post"""
        con = sqlite3.connect(db_name)
        q = con.execute(sql)
        data = q.fetchall()
        return [Post(*row) for row in data]
