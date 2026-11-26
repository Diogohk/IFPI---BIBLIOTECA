from flask import Blueprint, render_template, request, redirect, url_for, flash
from app.extensions import db
from app.models.exemplar import Exemplar
from app.models.livro import Livro
from app.routes.dashboard import login_obrigatorio

exemplares_bp = Blueprint("exemplares", __name__)
STATUS_VALIDOS = {"disponivel", "emprestado", "manutencao"}

@exemplares_bp.route("/exemplares", methods=["GET", "POST"])
@login_obrigatorio
def cadastrar_exemplar():
    livros = Livro.query.order_by(Livro.titulo.asc()).all()
    if request.method == "POST":
        idlivro = request.form.get("idlivro", type=int)
        codigo = request.form.get("codigo", "").strip()
        status = request.form.get("status", "").strip()
        livro = db.session.get(Livro, idlivro) if idlivro else None
        if not livro or not codigo or status not in STATUS_VALIDOS:
            flash("Selecione um livro e informe código e situação válidos.", "error")
        elif Exemplar.query.filter_by(codigo=codigo).first():
            flash("Já existe um exemplar com esse código.", "error")
        else:
            db.session.add(Exemplar(idlivro=idlivro, codigo=codigo, status=status))
            db.session.commit()
            flash("Exemplar cadastrado com sucesso!", "success")
            return redirect(url_for("exemplares.listar_exemplares"))
    return render_template("exemplares.html", livros=livros, exemplar=None)

@exemplares_bp.route("/exemplares/listar")
@login_obrigatorio
def listar_exemplares():
    exemplares = Exemplar.query.join(Livro).order_by(Livro.titulo.asc(), Exemplar.codigo.asc()).all()
    return render_template("listar_exemplares.html", exemplares=exemplares)

@exemplares_bp.route("/exemplares/<int:idexemplar>/editar", methods=["GET", "POST"])
@login_obrigatorio
def editar_exemplar(idexemplar):
    exemplar = db.get_or_404(Exemplar, idexemplar)
    livros = Livro.query.order_by(Livro.titulo.asc()).all()
    if request.method == "POST":
        idlivro = request.form.get("idlivro", type=int)
        codigo = request.form.get("codigo", "").strip()
        status = request.form.get("status", "").strip()
        livro = db.session.get(Livro, idlivro) if idlivro else None
        duplicado = Exemplar.query.filter(Exemplar.codigo == codigo, Exemplar.idexemplar != idexemplar).first()
        if not livro or not codigo or status not in STATUS_VALIDOS:
            flash("Selecione um livro e informe código e situação válidos.", "error")
        elif duplicado:
            flash("Outro exemplar já utiliza esse código.", "error")
        else:
            exemplar.idlivro, exemplar.codigo, exemplar.status = idlivro, codigo, status
            db.session.commit()
            flash("Exemplar atualizado com sucesso!", "success")
            return redirect(url_for("exemplares.listar_exemplares"))
    return render_template("exemplares.html", livros=livros, exemplar=exemplar)

@exemplares_bp.route("/exemplares/<int:idexemplar>/excluir", methods=["POST"])
@login_obrigatorio
def excluir_exemplar(idexemplar):
    exemplar = db.get_or_404(Exemplar, idexemplar)
    db.session.delete(exemplar)
    db.session.commit()
    flash("Exemplar excluído com sucesso.", "success")
    return redirect(url_for("exemplares.listar_exemplares"))
