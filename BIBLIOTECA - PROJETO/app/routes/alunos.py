import re

from flask import Blueprint, render_template, request, redirect, url_for, flash
from app.extensions import db
from app.models.aluno import Aluno
from app.models.emprestimo import Emprestimo
from app.routes.dashboard import login_obrigatorio

alunos_bp = Blueprint("alunos", __name__)


def validar_dados_aluno(matricula, nome, email, telefone, matricula_atual=None):
    if not matricula or not nome:
        return "Preencha os campos obrigatórios: matrícula e nome."
    if len(matricula) > 20 or len(nome) > 150:
        return "Matrícula deve ter até 20 caracteres e nome até 150 caracteres."
    if email and (len(email) > 254 or not re.fullmatch(r"[^@\s]+@[^@\s]+\.[^@\s]+", email)):
        return "Informe um endereço de e-mail válido com até 254 caracteres."
    if telefone and (
        len(telefone) > 20
        or not re.fullmatch(r"\+?[0-9\s().-]+", telefone)
        or not 10 <= len(re.sub(r"\D", "", telefone)) <= 13
    ):
        return "Informe um telefone válido, com 10 a 13 dígitos."
    existente = db.session.get(Aluno, matricula)
    if existente and matricula != matricula_atual:
        return "Esta matrícula já está cadastrada. Informe outra matrícula."
    return None


@alunos_bp.route("/alunos", methods=["GET", "POST"])
@login_obrigatorio
def cadastrar_aluno():
    if request.method == "POST":
        matricula = request.form.get("matricula", "").strip()
        nome = request.form.get("nome", "").strip()
        email = request.form.get("email", "").strip() or None
        telefone = request.form.get("telefone", "").strip() or None

        erro = validar_dados_aluno(matricula, nome, email, telefone)
        if erro:
            flash(erro, "error")
        else:
            db.session.add(Aluno(matricula=matricula, nome=nome, email=email, telefone=telefone))
            db.session.commit()
            flash("Aluno cadastrado com sucesso!", "success")
            return redirect(url_for("alunos.cadastrar_aluno"))

    return render_template("alunos.html", aluno=None)


@alunos_bp.route("/alunos/listar", methods=["GET"])
@login_obrigatorio
def listar_alunos():
    alunos = Aluno.query.order_by(Aluno.nome.asc()).all()
    return render_template("listar_alunos.html", alunos=alunos)


@alunos_bp.route("/alunos/<string:matricula>/editar", methods=["GET", "POST"])
@login_obrigatorio
def editar_aluno(matricula):
    aluno = db.get_or_404(Aluno, matricula)
    if request.method == "POST":
        nome = request.form.get("nome", "").strip()
        email = request.form.get("email", "").strip() or None
        telefone = request.form.get("telefone", "").strip() or None

        erro = validar_dados_aluno(aluno.matricula, nome, email, telefone, matricula_atual=aluno.matricula)
        if erro:
            flash(erro, "error")
        else:
            aluno.nome, aluno.email, aluno.telefone = nome, email, telefone
            db.session.commit()
            flash("Dados do aluno atualizados com sucesso!", "success")
            return redirect(url_for("alunos.listar_alunos"))

    return render_template("alunos.html", aluno=aluno)


@alunos_bp.route("/alunos/<string:matricula>/excluir", methods=["POST"])
@login_obrigatorio
def excluir_aluno(matricula):
    aluno = db.get_or_404(Aluno, matricula)
    if Emprestimo.query.filter_by(aluno_matricula=matricula).first():
        flash("Não é possível excluir este aluno porque existem empréstimos vinculados ao seu histórico.", "error")
    else:
        db.session.delete(aluno)
        db.session.commit()
        flash("Aluno excluído com sucesso.", "success")
    return redirect(url_for("alunos.listar_alunos"))
