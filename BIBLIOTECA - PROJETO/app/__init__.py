import os
from flask import Flask, redirect, url_for, session
from app.extensions import db, csrf
from app.config import Config


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    app.config["SESSION_COOKIE_HTTPONLY"] = True
    app.config["SESSION_COOKIE_SAMESITE"] = "Lax"
    app.config["MAX_CONTENT_LENGTH"] = 3 * 1024 * 1024
    app.config["UPLOAD_FOLDER"] = os.path.join(app.instance_path, "uploads", "funcionarios")
    os.makedirs(app.config["UPLOAD_FOLDER"], exist_ok=True)

    db.init_app(app)
    csrf.init_app(app)

    from app import models
    from app.routes.login import login_bp
    from app.routes.dashboard import dashboard_bp
    from app.routes.cadastro import cadastro_bp
    from app.routes.alunos import alunos_bp
    from app.routes.exemplares import exemplares_bp
    from app.routes.funcionarios import funcionarios_bp

    app.register_blueprint(login_bp)
    app.register_blueprint(dashboard_bp)
    app.register_blueprint(cadastro_bp)
    app.register_blueprint(alunos_bp)
    app.register_blueprint(exemplares_bp)
    app.register_blueprint(funcionarios_bp)

    with app.app_context():
        db.create_all()
        from app.migrations import aplicar_migracoes_automaticas
        aplicar_migracoes_automaticas()

    @app.route("/")
    def index():
        return redirect(url_for("dashboard.inicio") if session.get("funcionario_id")
                        else url_for("login.entrar"))

    return app
