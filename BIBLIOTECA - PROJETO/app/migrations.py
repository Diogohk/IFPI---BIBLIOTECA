from sqlalchemy import inspect, text
from sqlalchemy.exc import SQLAlchemyError

from app.extensions import db


def _adicionar_coluna_se_ausente(tabela, nome, definicao):
    inspector = inspect(db.engine)
    if not inspector.has_table(tabela):
        return
    colunas = {coluna["name"] for coluna in inspector.get_columns(tabela)}
    if nome in colunas:
        return
    try:
        with db.engine.begin() as conexao:
            conexao.execute(text(
                f"ALTER TABLE {tabela} ADD COLUMN {nome} {definicao}"
            ))
    except SQLAlchemyError:
        # Outra instância pode ter aplicado a mesma migração durante a inicialização.
        colunas_atuais = {
            coluna["name"] for coluna in inspect(db.engine).get_columns(tabela)
        }
        if nome not in colunas_atuais:
            raise


def aplicar_migracoes_automaticas():
    """Aplica alterações pequenas e idempotentes necessárias à versão atual."""
    _adicionar_coluna_se_ausente("livros", "capa_url", "TEXT NULL")
    _adicionar_coluna_se_ausente("funcionarios", "foto_perfil", "VARCHAR(255) NULL")
    _adicionar_coluna_se_ausente(
        "funcionarios", "is_admin", "BOOLEAN NOT NULL DEFAULT 0"
    )

    if not inspect(db.engine).has_table("funcionarios"):
        return

    # Em bancos antigos, promove o funcionário mais antigo caso ainda não exista
    # administrador. Isso evita bloquear a gestão depois da atualização.
    with db.engine.begin() as conexao:
        total_admins = conexao.execute(text(
            "SELECT COUNT(*) FROM funcionarios WHERE is_admin = 1"
        )).scalar()
        if not total_admins:
            primeiro_id = conexao.execute(text(
                "SELECT MIN(idfuncionario) FROM funcionarios"
            )).scalar()
            if primeiro_id is not None:
                conexao.execute(
                    text("UPDATE funcionarios SET is_admin = 1 WHERE idfuncionario = :id"),
                    {"id": primeiro_id},
                )
