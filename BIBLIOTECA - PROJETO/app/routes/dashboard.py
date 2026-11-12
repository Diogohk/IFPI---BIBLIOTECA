from functools import wraps
from flask import Blueprint, render_template, session, redirect, url_for

dashboard_bp = Blueprint("dashboard", __name__)

def login_obrigatorio(view):
    @wraps(view)
    def wrapped(*args, **kwargs):
        if not session.get("funcionario_id"):
            return redirect(url_for("login.entrar"))
        return view(*args, **kwargs)
    return wrapped

@dashboard_bp.route("/dashboard")
@login_obrigatorio
def inicio():
    return render_template("dashboard.html", nome=session.get("funcionario_nome", "Funcionário"))
