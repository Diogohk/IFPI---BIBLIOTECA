from flask import Flask
from app.extensions import db, csrf
from app.config import Config

def create_app():
    app = Flask(__name__)
    
    app.config.from_object(Config)

    db.init_app(app)
    csrf.init_app(app)

    from app import models

    return app

