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
            flash("Matrícula e nome são obrigatórios.", "error")
        elif db.session.get(Aluno, matricula):
            flash("Esta matrícula já está cadastrada.", "error")
        else:
            db.session.add(Aluno(matricula=matricula, nome=nome, email=email, telefone=telefone))
            db.session.commit()
            flash("Aluno cadastrado com sucesso!", "success")
            return redirect(url_for("alunos.cadastrar_aluno"))
    return render_template("alunos.html")
