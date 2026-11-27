from sqlalchemy import inspect, text
from sqlalchemy.exc import SQLAlchemyError

from app.extensions import db


def aplicar_migracoes_automaticas():
    """Aplica migrações pequenas e idempotentes necessárias ao funcionamento atual."""
    inspector = inspect(db.engine)

    if not inspector.has_table("livros"):
        return

    colunas = {coluna["name"] for coluna in inspector.get_columns("livros")}
    if "capa_url" in colunas:
        return

    try:
        with db.engine.begin() as conexao:
            conexao.execute(text("ALTER TABLE livros ADD COLUMN capa_url TEXT NULL"))
    except SQLAlchemyError:
        # Protege contra duas instâncias iniciando ao mesmo tempo.
        # Só ignora a falha se outra instância já tiver criado a coluna.
        inspector_atualizado = inspect(db.engine)
        colunas_atuais = {
            coluna["name"] for coluna in inspector_atualizado.get_columns("livros")
        }
        if "capa_url" not in colunas_atuais:
            raise
