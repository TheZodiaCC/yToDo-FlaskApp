import db


class Config:
    SQLALCHEMY_DATABASE_URI = f"mysql://{db.db_login}:{db.db_password}@{db.db_address}/{db.db_database}"