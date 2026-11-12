from flask import Flask, redirect, url_for, session
from app.extensions import db, csrf
from app.config import Config

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    app.config["SESSION_COOKIE_HTTPONLY"] = True
    app.config["SESSION_COOKIE_SAMESITE"] = "Lax"
    db.init_app(app)
    csrf.init_app(app)

    from app import models
    from app.routes.login import login_bp
    from app.routes.dashboard import dashboard_bp
    from app.routes.cadastro import cadastro_bp
    from app.routes.alunos import alunos_bp

    app.register_blueprint(login_bp)
    app.register_blueprint(dashboard_bp)
    app.register_blueprint(cadastro_bp)
    app.register_blueprint(alunos_bp)

    @app.route("/")
    def index():
        return redirect(url_for("dashboard.inicio") if session.get("funcionario_id")
                        else url_for("login.entrar"))
    return app
