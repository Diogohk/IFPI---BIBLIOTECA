import requests
from urllib.parse import urlparse
from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify, current_app
from app.extensions import db
from app.models.livro import Livro
from app.models.exemplar import Exemplar
from app.routes.dashboard import login_obrigatorio

cadastro_bp = Blueprint("cadastro", __name__)


@cadastro_bp.get("/api/google-books")
@login_obrigatorio
def pesquisar_google_books():
    termo = request.args.get("q", "").strip()
    if not termo:
        return jsonify({"error": "Informe um ISBN ou título para pesquisar."}), 400
    if len(termo) > 200:
        return jsonify({"error": "A pesquisa deve ter no máximo 200 caracteres."}), 400

    api_key = current_app.config.get("GOOGLE_BOOKS_API_KEY")
    if not api_key:
        return jsonify({"error": "A chave do Google Books não está configurada no servidor."}), 503

    try:
        resposta = requests.get(
            "https://www.googleapis.com/books/v1/volumes",
            params={"q": termo, "maxResults": 6, "key": api_key},
            timeout=10,
        )
    except requests.Timeout:
        current_app.logger.warning("Tempo limite excedido ao consultar Google Books.")
        return jsonify({"error": "O Google Books demorou para responder. Tente novamente."}), 504
    except requests.ConnectionError:
        current_app.logger.warning("Falha de conexão com Google Books.")
        return jsonify({"error": "Não foi possível conectar ao Google Books. Verifique a internet do servidor."}), 502
    except requests.RequestException as erro:
        current_app.logger.warning("Falha HTTP ao consultar Google Books (%s).", type(erro).__name__)
        return jsonify({"error": "O servidor não conseguiu concluir a consulta ao Google Books."}), 502

    try:
        dados = resposta.json()
    except ValueError:
        current_app.logger.warning("Google Books retornou JSON inválido (HTTP %s).", resposta.status_code)
        return jsonify({"error": "O Google Books retornou uma resposta inválida."}), 502

    if not resposta.ok:
        erro_api = dados.get("error", {}) if isinstance(dados, dict) else {}
        motivos = [
            item.get("reason", "")
            for item in erro_api.get("errors", [])
            if isinstance(item, dict)
        ]
        motivo = next((item for item in motivos if item), "")
        mensagem_google = erro_api.get("message", "")
        current_app.logger.warning(
            "Google Books recusou a consulta (HTTP %s, motivo: %s).",
            resposta.status_code,
            motivo or "não informado",
        )

        if resposta.status_code == 403:
            if motivo in ("accessNotConfigured", "serviceDisabled"):
                mensagem = "A Books API não está habilitada no projeto Google Cloud associado à chave."
            elif motivo in ("keyInvalid", "invalid"):
                mensagem = "A chave do Google Books é inválida. Confira GOOGLE_BOOKS_API_KEY no arquivo .env."
            elif motivo in ("ipRefererBlocked", "refererBlocked"):
                mensagem = "A chave está bloqueada pelas restrições de aplicativo. Revise as restrições da chave no Google Cloud."
            elif motivo in ("dailyLimitExceeded", "quotaExceeded", "rateLimitExceeded"):
                mensagem = "A cota ou o limite de consultas do Google Books foi atingido."
            else:
                mensagem = "O Google Cloud recusou a chave ou a requisição. Confira a Books API e as restrições da chave."
            return jsonify({"error": mensagem, "status": resposta.status_code}), 502

        if resposta.status_code == 429:
            return jsonify({
                "error": "O limite de consultas ao Google Books foi atingido. Tente novamente mais tarde.",
                "status": resposta.status_code,
            }), 429

        return jsonify({
            "error": f"O Google Books retornou um erro HTTP {resposta.status_code}. {mensagem_google[:180]}",
            "status": resposta.status_code,
        }), 502

    return jsonify(dados)


def isbn_valido(valor):
    isbn = (valor or "").replace("-", "").replace(" ", "").upper()
    if len(isbn) == 10 and isbn[:9].isdigit() and (isbn[9].isdigit() or isbn[9] == "X"):
        return sum((10 if c == "X" else int(c)) * (10-i) for i, c in enumerate(isbn)) % 11 == 0
    if len(isbn) == 13 and isbn.isdigit():
        return sum(int(c) * (1 if i % 2 == 0 else 3) for i, c in enumerate(isbn)) % 10 == 0
    return False


def capa_google_valida(valor):
    if not valor:
        return None
    if len(valor) > 2048:
        return False
    try:
        parsed = urlparse(valor)
    except ValueError:
        return False
    hosts_permitidos = {"books.google.com", "books.googleusercontent.com"}
    if parsed.scheme != "https" or parsed.hostname not in hosts_permitidos:
        return False
    if parsed.username or parsed.password:
        return False
    return valor


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
        capa_url = capa_google_valida(request.form.get("capa_url", "").strip())

        if not titulo or not autor or not isbn:
            flash("Preencha título, autor e ISBN.", "error")
        elif not isbn_valido(isbn):
            flash("O ISBN informado é inválido.", "error")
        elif ano_txt and (ano is None or not 1 <= ano <= 2100):
            flash("Informe um ano válido entre 1 e 2100.", "error")
        elif capa_url is False:
            flash("A capa selecionada não possui um endereço válido do Google Books.", "error")
        elif Livro.query.filter_by(isbn=isbn).first():
            flash("Já existe um livro cadastrado com esse ISBN.", "error")
        else:
            db.session.add(Livro(
                titulo=titulo, autor=autor, isbn=isbn, editora=editora,
                ano=ano, capa_url=capa_url
            ))
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
        capa_enviada = request.form.get("capa_url", "").strip()
        capa_url = capa_google_valida(capa_enviada) if capa_enviada else livro.capa_url
        duplicado = Livro.query.filter(Livro.isbn == isbn, Livro.idlivro != idlivro).first() if isbn else None

        if not titulo or not autor or not isbn:
            flash("Preencha título, autor e ISBN.", "error")
        elif not isbn_valido(isbn):
            flash("O ISBN informado é inválido.", "error")
        elif ano_txt and (ano is None or not 1 <= ano <= 2100):
            flash("Informe um ano válido entre 1 e 2100.", "error")
        elif capa_url is False:
            flash("A capa selecionada não possui um endereço válido do Google Books.", "error")
        elif duplicado:
            flash("Outro livro já utiliza esse ISBN.", "error")
        else:
            livro.titulo, livro.autor, livro.isbn = titulo, autor, isbn
            livro.editora, livro.ano, livro.capa_url = editora, ano, capa_url
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
