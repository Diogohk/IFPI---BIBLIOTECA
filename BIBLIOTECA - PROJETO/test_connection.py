from app import create_app
from app.extensions import db
from sqlalchemy import text

app = create_app()

with app.app_context():
    try:
        db.session.execute(text("SELECT 1"))
        print("Conexão com MySQL estabelecida!")

    except Exception as erro:
        print("Falha na conexão com MySQL:")
        print(erro)
    finally:
        db.session.remove()