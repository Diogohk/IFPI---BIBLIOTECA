from sqlalchemy import inspect, text
from sqlalchemy.exc import SQLAlchemyError

from app.extensions import db


def _colunas(tabela):
    if not inspect(db.engine).has_table(tabela):
        return set()
    return {coluna["name"] for coluna in inspect(db.engine).get_columns(tabela)}


def _adicionar_coluna_se_ausente(tabela, nome, definicao):
    if nome in _colunas(tabela):
        return
    if not inspect(db.engine).has_table(tabela):
        return

    try:
        with db.engine.begin() as conexao:
            conexao.execute(text(
                f"ALTER TABLE {tabela} ADD COLUMN {nome} {definicao}"
            ))
    except SQLAlchemyError:
        # Outra instância pode ter aplicado a mesma migração simultaneamente.
        if nome not in _colunas(tabela):
            raise


def _garantir_indice_unico(tabela, nome_indice, coluna):
    inspetor = inspect(db.engine)
    if not inspetor.has_table(tabela):
        return

    for indice in inspetor.get_indexes(tabela):
        if indice.get("unique") and indice.get("column_names") == [coluna]:
            return
    for restricao in inspetor.get_unique_constraints(tabela):
        if restricao.get("column_names") == [coluna]:
            return

    duplicado = db.session.execute(text(
        f"SELECT {coluna}, COUNT(*) AS total FROM {tabela} "
        f"WHERE {coluna} IS NOT NULL AND {coluna} <> '' "
        f"GROUP BY {coluna} HAVING COUNT(*) > 1 LIMIT 1"
    )).first()
    if duplicado:
        raise RuntimeError(
            f"Não foi possível criar a restrição única em {tabela}.{coluna}: "
            f"o valor '{duplicado[0]}' está repetido. Corrija os registros "
            "duplicados no banco e inicie a aplicação novamente."
        )

    with db.engine.begin() as conexao:
        conexao.execute(text(
            f"ALTER TABLE {tabela} ADD UNIQUE INDEX {nome_indice} ({coluna})"
        ))


def _migrar_isbn_livros():
    if not inspect(db.engine).has_table("livros"):
        return
    _adicionar_coluna_se_ausente("livros", "isbn", "VARCHAR(17) NULL")
    _garantir_indice_unico("livros", "uq_livros_isbn", "isbn")


def _migrar_codigo_exemplares():
    if not inspect(db.engine).has_table("exemplares"):
        return

    _adicionar_coluna_se_ausente("exemplares", "codigo", "VARCHAR(30) NULL")

    # Registros antigos recebem um código determinístico baseado na chave primária.
    with db.engine.begin() as conexao:
        conexao.execute(text(
            "UPDATE exemplares SET codigo = CONCAT('EX-', idexemplar) "
            "WHERE codigo IS NULL OR codigo = ''"
        ))

    _garantir_indice_unico("exemplares", "uq_exemplares_codigo", "codigo")

    # Depois de preencher os registros antigos, o campo passa a ser obrigatório.
    with db.engine.begin() as conexao:
        conexao.execute(text(
            "ALTER TABLE exemplares MODIFY codigo VARCHAR(30) NOT NULL"
        ))


def aplicar_migracoes_automaticas():
    """Aplica migrações idempotentes necessárias à versão atual do sistema."""
    _migrar_isbn_livros()
    _migrar_codigo_exemplares()

    _adicionar_coluna_se_ausente("livros", "capa_url", "TEXT NULL")
    _adicionar_coluna_se_ausente("funcionarios", "foto_perfil", "VARCHAR(255) NULL")
    _adicionar_coluna_se_ausente(
        "funcionarios", "is_admin", "BOOLEAN NOT NULL DEFAULT 0"
    )

    if not inspect(db.engine).has_table("funcionarios"):
        return

    # Em bancos antigos sem administrador, promove o funcionário mais antigo.
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
                    text(
                        "UPDATE funcionarios SET is_admin = 1 "
                        "WHERE idfuncionario = :id"
                    ),
                    {"id": primeiro_id},
                )
