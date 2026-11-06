from app.extensions import db


class Aluno(db.Model):
    __tablename__ = "alunos"

    matricula = db.Column(db.String(20), primary_key=True)
    nome = db.Column(db.String(150), nullable=False)
    email = db.Column(db.String(254), nullable=True)
    telefone = db.Column(db.String(20), nullable=True)