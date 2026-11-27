import os
import uuid
from functools import wraps

from flask import (
    Blueprint, abort, current_app, flash, redirect, render_template,
    request, send_from_directory, session, url_for
)
from werkzeug.security import generate_password_hash
from app.extensions import db
from app.models.funcionario import Funcionario
from app.models.emprestimo import Emprestimo
from app.routes.dashboard import login_obrigatorio

funcionarios_bp = Blueprint("funcionarios", __name__, url_prefix="/funcionarios")
EXTENSOES_IMAGEM = {".jpg": "jpeg", ".jpeg": "jpeg", ".png": "png", ".webp": "webp"}


def administrador_obrigatorio(view):
    @wraps(view)
    @login_obrigatorio
    def wrapped(*args, **kwargs):
        funcionario = db.session.get(Funcionario, session.get("funcionario_id"))
        if not funcionario or not funcionario.is_admin:
            abort(403)
        return view(*args, **kwargs)
    return wrapped


def salvar_foto(arquivo, foto_atual=None):
    if not arquivo or not arquivo.filename:
        return foto_atual, None
    extensao = os.path.splitext(arquivo.filename.lower())[1]
    tipo = EXTENSOES_IMAGEM.get(extensao)
    if not tipo:
        return foto_atual, "Use uma imagem JPG, PNG ou WEBP."
    conteudo = arquivo.read(16)
    arquivo.seek(0)
    valido = (
        (tipo == "jpeg" and conteudo.startswith(bytes.fromhex("FFD8FF")))
        or (tipo == "png" and conteudo.startswith(bytes.fromhex("89504E470D0A1A0A")))
        or (tipo == "webp" and conteudo.startswith(b"RIFF") and conteudo[8:12] == b"WEBP")
    )
    if not valido:
        return foto_atual, "O arquivo enviado não parece ser uma imagem válida."
    arquivo.seek(0, os.SEEK_END)
    tamanho = arquivo.tell()
    arquivo.seek(0)
    if tamanho > 2 * 1024 * 1024:
        return foto_atual, "A foto deve ter no máximo 2 MB."
    nome = f"{uuid.uuid4().hex}{extensao}"
    os.makedirs(current_app.config["UPLOAD_FOLDER"], exist_ok=True)
    arquivo.save(os.path.join(current_app.config["UPLOAD_FOLDER"], nome))
    return nome, None


def excluir_foto(nome):
    if not nome or os.path.basename(nome) != nome:
        return
    caminho = os.path.join(current_app.config["UPLOAD_FOLDER"], nome)
    if os.path.isfile(caminho):
        os.remove(caminho)


@funcionarios_bp.get("/foto/<path:filename>")
@login_obrigatorio
def foto_funcionario(filename):
    return send_from_directory(current_app.config["UPLOAD_FOLDER"], filename)


@funcionarios_bp.route("/listar")
@administrador_obrigatorio
def listar_funcionarios():
    funcionarios = Funcionario.query.order_by(Funcionario.nome.asc()).all()
    return render_template("listar_funcionarios.html", funcionarios=funcionarios)


@funcionarios_bp.route("/novo", methods=["GET", "POST"])
@administrador_obrigatorio
def cadastrar_funcionario():
    if request.method == "POST":
        matricula = request.form.get("matricula", "").strip()
        nome = request.form.get("nome", "").strip()
        cargo = request.form.get("cargo", "").strip()
        senha = request.form.get("senha", "")
        confirmacao = request.form.get("confirmacao_senha", "")

        if not matricula or not nome or not cargo or not senha:
            flash("Preencha todos os campos obrigatórios.", "error")
        elif len(matricula) > 20 or len(nome) > 150 or len(cargo) > 80:
            flash("Confira os limites de caracteres dos campos.", "error")
        elif Funcionario.query.filter_by(matricula=matricula).first():
            flash("Já existe um funcionário com essa matrícula.", "error")
        elif len(senha) < 8:
            flash("A senha precisa ter pelo menos 8 caracteres.", "error")
        elif senha != confirmacao:
            flash("As senhas não coincidem.", "error")
        else:
            foto, erro_foto = salvar_foto(request.files.get("foto"))
            if erro_foto:
                flash(erro_foto, "error")
            else:
                funcionario = Funcionario(
                    matricula=matricula,
                    nome=nome,
                    cargo=cargo,
                    senha_hash=generate_password_hash(senha),
                    foto_perfil=foto,
                    is_admin=False,
                )
                db.session.add(funcionario)
                db.session.commit()
                flash("Funcionário cadastrado com sucesso.", "success")
                return redirect(url_for("funcionarios.listar_funcionarios"))

    return render_template("funcionario.html", funcionario=None)


@funcionarios_bp.route("/<int:idfuncionario>/editar", methods=["GET", "POST"])
@administrador_obrigatorio
def editar_funcionario(idfuncionario):
    funcionario = db.get_or_404(Funcionario, idfuncionario)
    if request.method == "POST":
        matricula = request.form.get("matricula", "").strip()
        nome = request.form.get("nome", "").strip()
        cargo = request.form.get("cargo", "").strip()
        senha = request.form.get("senha", "")
        confirmacao = request.form.get("confirmacao_senha", "")
        duplicado = Funcionario.query.filter(
            Funcionario.matricula == matricula,
            Funcionario.idfuncionario != idfuncionario
        ).first()

        if not matricula or not nome or not cargo:
            flash("Preencha matrícula, nome e cargo.", "error")
        elif len(matricula) > 20 or len(nome) > 150 or len(cargo) > 80:
            flash("Confira os limites de caracteres dos campos.", "error")
        elif duplicado:
            flash("Essa matrícula já pertence a outro funcionário.", "error")
        elif senha and len(senha) < 8:
            flash("A nova senha precisa ter pelo menos 8 caracteres.", "error")
        elif senha and senha != confirmacao:
            flash("As senhas não coincidem.", "error")
        else:
            foto_antiga = funcionario.foto_perfil
            foto, erro_foto = salvar_foto(request.files.get("foto"), foto_antiga)
            if erro_foto:
                flash(erro_foto, "error")
            else:
                funcionario.matricula = matricula
                funcionario.nome = nome
                funcionario.cargo = cargo
                funcionario.foto_perfil = foto
                if senha:
                    funcionario.senha_hash = generate_password_hash(senha)
                db.session.commit()
                if foto_antiga and foto_antiga != foto:
                    excluir_foto(foto_antiga)
                if funcionario.idfuncionario == session.get("funcionario_id"):
                    session["funcionario_nome"] = funcionario.nome
                    session["funcionario_cargo"] = funcionario.cargo
                    session["funcionario_foto"] = funcionario.foto_perfil
                flash("Funcionário atualizado com sucesso.", "success")
                return redirect(url_for("funcionarios.listar_funcionarios"))

    return render_template("funcionario.html", funcionario=funcionario)


@funcionarios_bp.post("/<int:idfuncionario>/excluir")
@administrador_obrigatorio
def excluir_funcionario(idfuncionario):
    funcionario = db.get_or_404(Funcionario, idfuncionario)
    if funcionario.idfuncionario == session.get("funcionario_id"):
        flash("Não é possível excluir a própria conta enquanto estiver conectado.", "error")
    elif funcionario.is_admin and Funcionario.query.filter_by(is_admin=True).count() <= 1:
        flash("O sistema precisa manter pelo menos um administrador.", "error")
    elif Emprestimo.query.filter_by(funcionario_idfuncionario=idfuncionario).first():
        flash("Não é possível excluir este funcionário porque há empréstimos registrados em seu nome.", "error")
    else:
        foto = funcionario.foto_perfil
        db.session.delete(funcionario)
        db.session.commit()
        excluir_foto(foto)
        flash("Funcionário excluído com sucesso.", "success")
    return redirect(url_for("funcionarios.listar_funcionarios"))


@funcionarios_bp.route("/perfil", methods=["GET", "POST"])
@login_obrigatorio
def meu_perfil():
    funcionario = db.get_or_404(Funcionario, session.get("funcionario_id"))
    if request.method == "POST":
        nome = request.form.get("nome", "").strip()
        cargo = request.form.get("cargo", "").strip()
        if not nome or not cargo or len(nome) > 150 or len(cargo) > 80:
            flash("Informe nome e cargo dentro dos limites permitidos.", "error")
        else:
            foto_antiga = funcionario.foto_perfil
            foto, erro_foto = salvar_foto(request.files.get("foto"), foto_antiga)
            if erro_foto:
                flash(erro_foto, "error")
                return render_template("perfil_funcionario.html", funcionario=funcionario)
            funcionario.nome = nome
            funcionario.cargo = cargo
            funcionario.foto_perfil = foto
            db.session.commit()
            if foto_antiga and foto_antiga != foto:
                excluir_foto(foto_antiga)
            session["funcionario_nome"] = nome
            session["funcionario_cargo"] = cargo
            session["funcionario_foto"] = foto
            flash("Perfil atualizado com sucesso.", "success")
            return redirect(url_for("funcionarios.meu_perfil"))
    return render_template("perfil_funcionario.html", funcionario=funcionario)
