#from main import database
from __init__ import database
import db


class User(database.Model):

    __tablename__ = db.db_users
    id = database.Column("user_id", database.Integer, primary_key=True)
    name = database.Column("nick")
    password = database.Column("password_hash")
    backup = database.Column("back_code")
    saw = database.Column("saw_code")
    #blocked = database.Column("blocked")


class ToDo(database.Model):

    __tablename__ = "things"
    id = database.Column("thing_id", database.Integer, primary_key=True)
    owner_id = database.Column("owner_id")
    title = database.Column("title")
    content = database.Column("content")
