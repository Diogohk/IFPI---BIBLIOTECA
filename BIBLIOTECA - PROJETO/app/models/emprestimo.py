from app.extensions import db


class Emprestimo(db.Model):
    __tablename__ = "emprestimos"

    idemprestimo = db.Column(db.Integer, primary_key=True, autoincrement=True)

    dataemprestimo = db.Column(db.Date, nullable=False)
    dataprevista = db.Column(db.Date, nullable=False)

    aluno_matricula = db.Column(
        db.String(20),
        db.ForeignKey("alunos.matricula"),
        nullable=False
    )

    exemplar_idexemplar = db.Column(
        db.Integer,
        db.ForeignKey("exemplares.idexemplar"),
        nullable=False
    )

    funcionario_idfuncionario = db.Column(
        db.Integer,
        db.ForeignKey("funcionarios.idfuncionario"),
        nullable=False
    )