from flask import Flask, render_template
from app.extensions import db, csrf
from app.config import Config


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    csrf.init_app(app)

    from app import models
    from app.routes.alunos import alunos_bp

    app.register_blueprint(alunos_bp)

    @app.route("/")
    def index():
        return render_template("alunos.html")

    return app