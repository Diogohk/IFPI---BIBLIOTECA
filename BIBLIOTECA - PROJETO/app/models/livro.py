from app.extensions import db


class Livro(db.Model):
    __tablename__ = "livros"

    idlivro = db.Column(db.Integer, primary_key=True, autoincrement=True)
    titulo = db.Column(db.String(255), nullable=False)
    autor = db.Column(db.String(150), nullable=False)
    editora = db.Column(db.String(120))
    ano = db.Column(db.Integer)