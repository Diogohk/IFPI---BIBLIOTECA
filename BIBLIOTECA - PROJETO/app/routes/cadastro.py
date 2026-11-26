from flask import Blueprint, render_template, request, redirect, url_for, flash
from sqlalchemy.exc import IntegrityError
from app.extensions import db
from app.models.livro import Livro
from app.models.exemplar import Exemplar
from app.routes.dashboard import login_obrigatorio

cadastro_bp = Blueprint("cadastro", __name__)

def isbn_valido(valor):
    isbn = (valor or "").replace("-", "").replace(" ", "").upper()
    if len(isbn) == 10 and (isbn[:9].isdigit()) and (isbn[9].isdigit() or isbn[9] == "X"):
        return sum((10 if c == "X" else int(c)) * (10-i) for i, c in enumerate(isbn)) % 11 == 0
    if len(isbn) == 13 and isbn.isdigit():
        return sum(int(c) * (1 if i % 2 == 0 else 3) for i, c in enumerate(isbn)) % 10 == 0
    return False

@cadastro_bp.route("/livros", methods=["GET", "POST"])
@login_obrigatorio
def cadastrar():
    if request.method == "POST":
        titulo = request.form.get("titulo", "").strip()
        autor = request.form.get("autor", "").strip()
        isbn = request.form.get("isbn", "").strip().replace("-", "").replace(" ", "") or None
        editora = request.form.get("editora", "").strip() or None
        ano_txt = request.form.get("ano_publicacao", "").strip()
        ano = int(ano_txt) if ano_txt.isdigit() else None

        if not titulo or not autor or not isbn:
            flash("Preencha título, autor e ISBN.", "error")
        elif not isbn_valido(isbn):
            flash("O ISBN informado é inválido.", "error")
        elif ano_txt and (ano is None or not 1 <= ano <= 2100):
            flash("Informe um ano válido entre 1 e 2100.", "error")
        elif Livro.query.filter_by(isbn=isbn).first():
            flash("Já existe um livro cadastrado com esse ISBN.", "error")
        else:
            db.session.add(Livro(titulo=titulo, autor=autor, isbn=isbn, editora=editora, ano=ano))
            db.session.commit()
            flash("Livro cadastrado com sucesso!", "success")
            return redirect(url_for("cadastro.listar_livros"))
    return render_template("cadastro.html", livro=None)

@cadastro_bp.route("/livros/listar")
@login_obrigatorio
def listar_livros():
    livros = Livro.query.order_by(Livro.titulo.asc()).all()
    return render_template("listar_livros.html", livros=livros)

@cadastro_bp.route("/livros/<int:idlivro>/editar", methods=["GET", "POST"])
@login_obrigatorio
def editar_livro(idlivro):
    livro = db.get_or_404(Livro, idlivro)
    if request.method == "POST":
        titulo = request.form.get("titulo", "").strip()
        autor = request.form.get("autor", "").strip()
        isbn = request.form.get("isbn", "").strip().replace("-", "").replace(" ", "") or None
        editora = request.form.get("editora", "").strip() or None
        ano_txt = request.form.get("ano_publicacao", "").strip()
        ano = int(ano_txt) if ano_txt.isdigit() else None
        duplicado = Livro.query.filter(Livro.isbn == isbn, Livro.idlivro != idlivro).first() if isbn else None
        if not titulo or not autor or not isbn:
            flash("Preencha título, autor e ISBN.", "error")
        elif not isbn_valido(isbn):
            flash("O ISBN informado é inválido.", "error")
        elif ano_txt and (ano is None or not 1 <= ano <= 2100):
            flash("Informe um ano válido entre 1 e 2100.", "error")
        elif duplicado:
            flash("Outro livro já utiliza esse ISBN.", "error")
        else:
            livro.titulo, livro.autor, livro.isbn = titulo, autor, isbn
            livro.editora, livro.ano = editora, ano
            db.session.commit()
            flash("Livro atualizado com sucesso!", "success")
            return redirect(url_for("cadastro.listar_livros"))
    return render_template("cadastro.html", livro=livro)

@cadastro_bp.route("/livros/<int:idlivro>/excluir", methods=["POST"])
@login_obrigatorio
def excluir_livro(idlivro):
    livro = db.get_or_404(Livro, idlivro)
    if Exemplar.query.filter_by(idlivro=idlivro).first():
        flash("Não é possível excluir uma obra que possui exemplares cadastrados. Exclua os exemplares primeiro.", "error")
    else:
        db.session.delete(livro)
        db.session.commit()
        flash("Livro excluído com sucesso.", "success")
    return redirect(url_for("cadastro.listar_livros"))
