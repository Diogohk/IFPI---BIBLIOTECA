from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from werkzeug.security import check_password_hash
from app.models.funcionario import Funcionario

login_bp = Blueprint("login", __name__)

@login_bp.route("/login", methods=["GET", "POST"])
def entrar():
    if session.get("funcionario_id"):
        return redirect(url_for("dashboard.inicio"))

    if request.method == "POST":
        matricula = request.form.get("matricula", "").strip()
        senha = request.form.get("senha", "")
        funcionario = Funcionario.query.filter_by(matricula=matricula).first()

        if funcionario and check_password_hash(funcionario.senha_hash, senha):
            session.clear()
            session["funcionario_id"] = funcionario.idfuncionario
            session["funcionario_nome"] = funcionario.nome
            return redirect(url_for("dashboard.inicio"))

        flash("Matrícula ou senha inválida.", "error")

    return render_template("login.html")

@login_bp.route("/sair", methods=["POST"])
def sair():
    session.clear()
    flash("Sessão encerrada.", "success")
    return redirect(url_for("login.entrar"))
