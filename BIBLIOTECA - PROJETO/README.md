Biblioteca IFPI — Sistema de Gerenciamento

Equipe: Guardiões da Galáxia
Instituição: Instituto Federal do Piauí (IFPI) — Campus Paulistana

Sobre o projeto

O Biblioteca IFPI é um sistema web desenvolvido para apoiar as atividades do Setor de Biblioteca do IFPI — Campus Paulistana. A aplicação é direcionada aos funcionários da biblioteca e permite, nesta etapa, acessar os formulários de cadastro de livros e alunos e consultar os alunos cadastrados.

O projeto está em desenvolvimento. Funcionalidades que ainda não estejam integradas e testadas — como cadastro de exemplares, empréstimos, devoluções, movimentações e estatísticas — não devem ser consideradas disponíveis.

Tecnologias

* Python 3.10 ou superior
* Flask
* Flask-SQLAlchemy e SQLAlchemy (ORM)
* MySQL e PyMySQL
* Flask-WTF (proteção CSRF)
* HTML, CSS e JavaScript
* XAMPP (opção para executar o MySQL localmente)

Requisitos

Antes de começar, instale:

* Python 3.10 ou superior
* Git
* MySQL (pode ser iniciado pelo XAMPP)
* Visual Studio Code ou outro editor de sua preferência

Instalação

1. Baixar o projeto

Abra o terminal e execute:

git clone https://github.com/Diogohk/IFPI---BIBLIOTECA.git

Entre na pasta do projeto:

cd "IFPI---BIBLIOTECA/BIBLIOTECA - PROJETO"

Se o nome ou a organização das pastas no seu computador estiver diferente, entre na pasta BIBLIOTECA - PROJETO antes de continuar.

2. Criar e ativar o ambiente virtual

No Windows, dentro da pasta BIBLIOTECA - PROJETO, execute:

python -m venv .venv

Ative o ambiente virtual:

.\.venv\Scripts\Activate.ps1

Se o PowerShell bloquear a ativação, abra o terminal Prompt de Comando (cmd) no VS Code e use:

.venv\Scripts\activate.bat

3. Instalar as dependências

Com o ambiente virtual ativado, execute:

python -m pip install --upgrade pip
pip install -r requirements.txt

Configuração do banco de dados

1. Inicie o serviço MySQL. Se estiver usando XAMPP, abra o painel do XAMPP e inicie MySQL.
2. Na pasta principal do projeto, localize .env.example.
3. Consulte esse arquivo para identificar os nomes das variáveis de configuração esperadas pela aplicação.
4. Crie uma cópia chamada .env e preencha os valores locais de conexão com o MySQL.
5. Nunca publique o arquivo .env, senhas ou outras credenciais no GitHub.
6. Consulte MIGRACAO_MARCO_4_5.sql e a documentação do projeto para confirmar se a migração precisa ser executada no banco antes de iniciar a aplicação.

Importante: os nomes exatos das variáveis do .env, o nome do banco de dados e os passos de importação da migração precisam corresponder aos arquivos de configuração atuais do projeto. Confira app/config.py e a documentação antes de preencher esses valores.

Como executar

Com o ambiente virtual ativado, o MySQL em execução e a configuração do banco concluída, execute na pasta principal:

python run.py

Depois, observe o endereço informado no terminal e abra-o no navegador.

Se ocorrer um erro, confira primeiro se o MySQL está iniciado, se o .env está preenchido corretamente e se as dependências foram instaladas.

Acesso de funcionário

O sistema é destinado aos funcionários da biblioteca.

O repositório contém o arquivo criar_funcionario.py, relacionado à criação de um funcionário. Antes de tentar entrar no sistema:

1. Confirme que o banco de dados está configurado e que a migração necessária foi aplicada.
2. Consulte as instruções de acesso em CONFIGURAR_ACESSO.md.
3. Verifique no código de criar_funcionario.py quais dados são solicitados para criar o funcionário e como o cadastro é realizado.
4. Execute o procedimento de criação conforme as instruções do próprio projeto.
5. Na tela de login, use os dados cadastrados para o funcionário.

Atenção: não existe neste README uma matrícula, usuário ou senha padrão confirmada. Não tente adivinhar credenciais. O identificador de login e o procedimento correto devem ser confirmados em CONFIGURAR_ACESSO.md, criar_funcionario.py e no código da rota de login. Nunca compartilhe senhas.

Arquivos importantes

Arquivo ou pasta	Finalidade
app/	Código da aplicação Flask
.env.example	Exemplo das configurações de ambiente
.gitignore	Arquivos que não devem ser enviados ao Git
CONFIGURAR_ACESSO.md	Orientações relacionadas ao acesso
criar_funcionario.py	Script relacionado à criação de funcionário
MIGRACAO_MARCO_4_5.sql	Script SQL de migração do banco
requirements.txt	Dependências Python
run.py	Arquivo de inicialização da aplicação
test_connection.py	Script de teste da conexão

Segurança

* Não envie credenciais, senhas ou o arquivo .env para o repositório.
* Mantenha o .env protegido e confira se ele está listado no .gitignore.
* Utilize os formulários da aplicação e suas validações.
* As operações com o banco devem seguir a implementação baseada em SQLAlchemy/ORM.
* Não compartilhe credenciais de funcionários.

Situação do desenvolvimento

O projeto está em desenvolvimento. Consulte a aplicação e a documentação atualizadas para identificar quais funcionalidades estão implementadas e testadas.

Equipe

Guardiões da Galáxia
Instituto Federal do Piauí (IFPI) — Campus Paulistana