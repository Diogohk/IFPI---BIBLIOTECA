from flask import Blueprint, render_template, request, redirect, url_for, flash
from app.extensions import db
from app.models.aluno import Aluno

alunos_bp = Blueprint("alunos", __name__)


@alunos_bp.route("/alunos", methods=["GET", "POST"])
def cadastrar_aluno():
    if request.method == "POST":
        matricula = request.form.get("matricula", "").strip()
        nome = request.form.get("nome", "").strip()
        email = request.form.get("email", "").strip() or None

        if not matricula or not nome:
            flash("Matrícula e nome são obrigatórios.")
            return redirect(url_for("alunos.cadastrar_aluno"))

        if db.session.get(Aluno, matricula):
            flash("Esta matrícula já está cadastrada.")
            return redirect(url_for("alunos.cadastrar_aluno"))

        aluno = Aluno(
            matricula=matricula,
            nome=nome,
            email=email
        )

        db.session.add(aluno)
        db.session.commit()

        flash("Aluno cadastrado com sucesso!")
        return redirect(url_for("alunos.cadastrar_aluno"))

    return render_template("alunos.html")