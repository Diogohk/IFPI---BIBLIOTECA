from app.extensions import db


class Exemplar(db.Model):
    __tablename__ = "exemplares"

    idexemplar = db.Column(db.Integer, primary_key=True, autoincrement=True)

    idlivro = db.Column(
        db.Integer,
        db.ForeignKey("livros.idlivro"),
        nullable=False
    )

    status = db.Column(db.String(20), nullable=False, default="disponivel")