from flask import Blueprint, render_template

cadastro_bp = Blueprint("cadastro", __name__)


@cadastro_bp.route("/cadastro", methods=["GET"])
def cadastrar():
    return render_template("cadastro.html")
