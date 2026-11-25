from getpass import getpass

from werkzeug.security import generate_password_hash

from app import create_app, db
from app.models.funcionario import Funcionario


def solicitar_dado(rotulo, limite, obrigatorio=True):
    while True:
        valor = input(f"{rotulo}: ").strip()
        if obrigatorio and not valor:
            print("Este campo é obrigatório.")
            continue
        if len(valor) > limite:
            print(f"Use no máximo {limite} caracteres.")
            continue
        return valor


def main():
    app = create_app()

    with app.app_context():
        try:
            # Cria as tabelas mapeadas caso ainda não existam.
            db.create_all()

            print("\n=== Cadastro de funcionário ===")
            print("Crie o acesso que será usado na tela de login.\n")

            matricula = solicitar_dado("Matrícula", 20)
            if Funcionario.query.filter_by(matricula=matricula).first():
                print("\nJá existe um funcionário com essa matrícula.")
                return

            nome = solicitar_dado("Nome completo", 150)
            cargo = solicitar_dado("Cargo", 80)

            while True:
                senha = getpass("Senha (mínimo 8 caracteres): ")
                confirmacao = getpass("Confirme a senha: ")

                if len(senha) < 8:
                    print("A senha precisa ter pelo menos 8 caracteres.")
                elif senha != confirmacao:
                    print("As senhas não coincidem.")
                else:
                    break

            funcionario = Funcionario(
                matricula=matricula,
                nome=nome,
                cargo=cargo,
                senha_hash=generate_password_hash(senha),
            )

            db.session.add(funcionario)
            db.session.commit()

            print("\nFuncionário cadastrado com sucesso.")
            print(f"Matrícula para login: {matricula}")
            print("A senha foi armazenada como hash. Guarde-a em local seguro.")

        except Exception as erro:
            db.session.rollback()
            print("\nNão foi possível cadastrar o funcionário.")
            print(f"Verifique a configuração do banco de dados. Detalhe: {erro}")


if __name__ == "__main__":
    main()
