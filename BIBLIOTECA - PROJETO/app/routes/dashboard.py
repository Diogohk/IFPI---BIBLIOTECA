from flask import Blueprint, render_template, session, redirect, url_for
from app.extensions import db
from app.models.aluno import Aluno
from app.models.exemplar import Exemplar
from app.models.livro import Livro

dashboard_bp = Blueprint("dashboard", __name__)


def login_obrigatorio(view):
    from functools import wraps

    @wraps(view)
    def wrapped(*args, **kwargs):
        if not session.get("funcionario_id"):
            return redirect(url_for("login.entrar"))
        return view(*args, **kwargs)
    return wrapped


@dashboard_bp.route("/dashboard")
@login_obrigatorio
def inicio():
    # Indicadores gerais e amostras para consulta rápida no painel.
    total_livros = Livro.query.count()
    total_alunos = Aluno.query.count()
    total_exemplares = Exemplar.query.count()
    exemplares_disponiveis = Exemplar.query.filter_by(status="disponivel").count()

    livros = Livro.query.order_by(Livro.idlivro.desc()).limit(5).all()
    alunos = Aluno.query.order_by(Aluno.nome.asc()).limit(5).all()
    exemplares = (
        Exemplar.query.join(Livro)
        .order_by(Exemplar.idexemplar.desc())
        .limit(5)
        .all()
    )

    return render_template(
        "dashboard.html",
        nome=session.get("funcionario_nome", "Funcionário"),
        total_livros=total_livros,
        total_alunos=total_alunos,
        total_exemplares=total_exemplares,
        exemplares_disponiveis=exemplares_disponiveis,
        livros=livros,
        alunos=alunos,
        exemplares=exemplares,
    )
