from flask import Blueprint, render_template, request, flash

login_bp = Blueprint("login", __name__)


@login_bp.route("/login", methods=["GET", "POST"])
def entrar():
    if request.method == "POST":
        # A validação de usuário e senha depende da integração com o banco.
        flash("A autenticação ainda não foi integrada ao sistema.", "info")

    return render_template("login.html")
