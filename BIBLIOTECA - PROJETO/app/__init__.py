from flask import Flask, redirect, url_for
from app.extensions import db, csrf
from app.config import Config


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    csrf.init_app(app)

    # Importar os modelos garante que o SQLAlchemy conheça todas as tabelas.
    from app import models

    # Registrar as rotas na ordem solicitada.
    from app.routes.login import login_bp
    from app.routes.cadastro import cadastro_bp
    from app.routes.alunos import alunos_bp

    app.register_blueprint(login_bp)
    app.register_blueprint(cadastro_bp)
    app.register_blueprint(alunos_bp)

    @app.route("/")
    def index():
        return redirect(url_for("login.login"))

    return app
