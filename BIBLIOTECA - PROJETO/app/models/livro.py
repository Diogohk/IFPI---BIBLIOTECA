from app.extensions import db

class Livro(db.Model):
    __tablename__ = "livros"

    idlivro = db.Column(db.Integer, primary_key=True, autoincrement=True)
    titulo = db.Column(db.String(255), nullable=False)
    autor = db.Column(db.String(150), nullable=False)
    isbn = db.Column(db.String(17), unique=True, nullable=True)
    editora = db.Column(db.String(120))
    ano = db.Column(db.Integer)
    capa_url = db.Column(db.Text, nullable=True)

    exemplares = db.relationship(
        "Exemplar", backref="livro", lazy=True, cascade="all, delete-orphan"
    )
