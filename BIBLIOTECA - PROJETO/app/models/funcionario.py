from app.extensions import db

class Funcionario(db.Model):
    __tablename__ = "funcionarios"

    idfuncionario = db.Column(db.Integer, primary_key=True, autoincrement=True)
    matricula = db.Column(db.String(20), nullable=False, unique=True, index=True)
    nome = db.Column(db.String(150), nullable=False)
    cargo = db.Column(db.String(80), nullable=False)
    senha_hash = db.Column(db.String(255), nullable=False)
