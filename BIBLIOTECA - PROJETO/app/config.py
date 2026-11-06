import os

class Config:
    SQLALCHEMY_DATABASE_URI = (
        "mysql+pymysql://usuario:senha@localhost/biblioteca"
    )

    SQLALCHEMY_TRACK_MODIFICATIONS = False