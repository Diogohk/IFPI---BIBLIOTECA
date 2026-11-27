import secrets

from flask import (
    Blueprint, current_app, flash, redirect, render_template,
    request, session, url_for
)
from werkzeug.security import check_password_hash, generate_password_hash

from app.extensions import db
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
            session["funcionario_cargo"] = funcionario.cargo
            session["funcionario_foto"] = funcionario.foto_perfil
            session["funcionario_admin"] = bool(funcionario.is_admin)
            return redirect(url_for("dashboard.inicio"))

        flash("Matrícula ou senha inválida.", "error")

    return render_template("login.html")


@login_bp.route("/cadastro-funcionario", methods=["GET", "POST"])
def cadastrar():
    if session.get("funcionario_id"):
        return redirect(url_for("dashboard.inicio"))

    codigo_configurado = current_app.config.get("CADASTRO_FUNCIONARIO_CODIGO", "").strip()

    if request.method == "POST":
        codigo = request.form.get("codigo_convite", "").strip()
        matricula = request.form.get("matricula", "").strip()
        nome = request.form.get("nome", "").strip()
        cargo = request.form.get("cargo", "").strip()
        senha = request.form.get("senha", "")
        confirmacao = request.form.get("confirmacao_senha", "")

        if not codigo_configurado:
            flash("O cadastro está desativado. Solicite ao administrador a configuração do código de convite.", "error")
        elif not secrets.compare_digest(codigo, codigo_configurado):
            flash("Código de convite inválido.", "error")
        elif not matricula or not nome or not cargo or not senha:
            flash("Preencha todos os campos obrigatórios.", "error")
        elif len(matricula) > 20 or len(nome) > 150 or len(cargo) > 80:
            flash("Confira os limites de caracteres dos campos.", "error")
        elif Funcionario.query.filter_by(matricula=matricula).first():
            flash("Já existe um funcionário com essa matrícula.", "error")
        elif len(senha) < 8:
            flash("A senha precisa ter pelo menos 8 caracteres.", "error")
        elif senha != confirmacao:
            flash("As senhas não coincidem.", "error")
        else:
            funcionario = Funcionario(
                matricula=matricula,
                nome=nome,
                cargo=cargo,
                senha_hash=generate_password_hash(senha),
                is_admin=False,
            )
            db.session.add(funcionario)
            db.session.commit()
            flash("Cadastro realizado. Agora entre com sua matrícula e senha.", "success")
            return redirect(url_for("login.entrar"))

    return render_template("cadastro_funcionario_publico.html", cadastro_ativo=bool(codigo_configurado))


@login_bp.route("/sair", methods=["POST"])
def sair():
    session.clear()
    flash("Sessão encerrada.", "success")
    return redirect(url_for("login.entrar"))
