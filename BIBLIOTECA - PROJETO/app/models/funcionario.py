from app.extensions import db


class Funcionario(db.Model):
    __tablename__ = "funcionarios"

    idfuncionario = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nome = db.Column(db.String(150), nullable=False)
    cargo = db.Column(db.String(80), nullable=False)