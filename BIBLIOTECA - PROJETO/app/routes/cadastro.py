from flask import Blueprint, render_template, request, flash
from app.routes.dashboard import login_obrigatorio

cadastro_bp = Blueprint("cadastro", __name__)

@cadastro_bp.route("/livros", methods=["GET", "POST"])
@login_obrigatorio
def cadastrar():
    if request.method == "POST":
        flash("O formulário está pronto, mas a gravação de livros ainda precisa ser integrada ao modelo.", "info")
    return render_template("cadastro.html")
