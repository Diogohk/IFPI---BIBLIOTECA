from app.extensions import db


class Devolucao(db.Model):
    __tablename__ = "devolucoes"

    iddevolucao = db.Column(db.Integer, primary_key=True, autoincrement=True)

    idemprestimo = db.Column(
        db.Integer,
        db.ForeignKey("emprestimos.idemprestimo"),
        nullable=False,
        unique=True
    )

    idfuncionario = db.Column(
        db.Integer,
        db.ForeignKey("funcionarios.idfuncionario"),
        nullable=False
    )

    datadevolucao = db.Column(db.Date, nullable=False)