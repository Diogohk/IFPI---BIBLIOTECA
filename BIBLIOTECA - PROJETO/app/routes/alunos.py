import re

from flask import Blueprint, render_template, request, redirect, url_for, flash
from app.extensions import db
from app.models.aluno import Aluno
from app.routes.dashboard import login_obrigatorio

alunos_bp = Blueprint("alunos", __name__)


@alunos_bp.route("/alunos", methods=["GET", "POST"])
@login_obrigatorio
def cadastrar_aluno():
    if request.method == "POST":
        matricula = request.form.get("matricula", "").strip()
        nome = request.form.get("nome", "").strip()
        email = request.form.get("email", "").strip() or None
        telefone = request.form.get("telefone", "").strip() or None

        if not matricula or not nome:
            flash("Preencha os campos obrigatórios: matrícula e nome.", "error")
        elif len(matricula) > 20 or len(nome) > 150:
            flash("Matrícula deve ter até 20 caracteres e nome até 150 caracteres.", "error")
        elif email and (len(email) > 254 or not re.fullmatch(r"[^@\s]+@[^@\s]+\.[^@\s]+", email)):
            flash("Informe um endereço de e-mail válido com até 254 caracteres.", "error")
        elif telefone and len(telefone) > 20:
            flash("O telefone deve ter até 20 caracteres.", "error")
        elif db.session.get(Aluno, matricula):
            flash("Esta matrícula já está cadastrada. Informe outra matrícula.", "error")
        else:
            db.session.add(
                Aluno(
                    matricula=matricula,
                    nome=nome,
                    email=email,
                    telefone=telefone,
                )
            )
            db.session.commit()
            flash("Aluno cadastrado com sucesso!", "success")
            return redirect(url_for("alunos.cadastrar_aluno"))

    return render_template("alunos.html")


@alunos_bp.route("/alunos/listar", methods=["GET"])
@login_obrigatorio
def listar_alunos():
    alunos = Aluno.query.order_by(Aluno.nome.asc()).all()
    return render_template("listar_alunos.html", alunos=alunos)
