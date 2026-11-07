Biblioteca IFPI — Sistema de Gerenciamento

Equipe: Guardiões da Galáxia
Instituição: Instituto Federal do Piauí (IFPI) — Campus Paulistana

Sobre o projeto

O Biblioteca IFPI é um sistema web desenvolvido para auxiliar o Setor de Biblioteca do IFPI — Campus Paulistana no gerenciamento de suas atividades.

O projeto busca tornar mais prático o registro e a consulta de informações dos alunos e contribuir para a redução de conflitos durante o processo de empréstimo e devolução de livros, especialmente aqueles relacionados às instabilidades do sistema atualmente utilizado.

A aplicação está inicialmente direcionada aos funcionários da biblioteca.

Objetivos

- Facilitar o cadastro e a consulta de alunos.
- Organizar o catálogo de livros.
- Controlar os exemplares disponíveis.
- Gerenciar empréstimos e devoluções.
- Manter os registros organizados em um banco de dados.
- Oferecer uma interface simples e acessível aos funcionários.

Tecnologias utilizadas

Tecnologia| Finalidade
Python| Linguagem principal
Flask| Framework web e gerenciamento das rotas
Flask-SQLAlchemy| Integração entre aplicação e banco de dados
SQLAlchemy| Mapeamento objeto-relacional (ORM)
MySQL| Sistema de gerenciamento de banco de dados
XAMPP| Ambiente local para execução do MySQL
PyMySQL| Conector entre Python e MySQL
HTML| Estrutura das páginas
CSS| Estilização das interfaces
JavaScript| Interatividade no navegador
Requests| Requisições HTTP e possível integração com APIs

Integração complementar

Está prevista a utilização da API pública do Google Books para auxiliar na obtenção de informações de livros por ISBN ou título.

Essa integração é complementar e não deve comprometer o desenvolvimento das funcionalidades principais.

Funcionalidades previstas

- Cadastro, consulta, edição e exclusão de alunos.
- Cadastro e gerenciamento de livros.
- Gerenciamento de exemplares.
- Registro de empréstimos.
- Registro de devoluções.
- Consulta de informações armazenadas no banco de dados.

As funcionalidades serão disponibilizadas progressivamente durante o desenvolvimento.

Estrutura do projeto

A estrutura modular planejada é:

BIBLIOTECA - PROJETO/
│
├── app/
│   ├── __init__.py
│   ├── config.py
│   ├── extensions.py
│   │
│   ├── models/
│   │   └── __init__.py
│   │
│   ├── routes/
│   │   └── __init__.py
│   │
│   ├── templates/
│   │
│   └── static/
│       ├── css/
│       ├── js/
│       └── img/
│
├── .env
├── .gitignore
├── requirements.txt
├── run.py
└── README.md

A estrutura acima representa a organização planejada e poderá ser ajustada conforme a implementação.

Requisitos para execução

- Python instalado.
- MySQL disponível localmente.
- XAMPP ou outro ambiente compatível para executar o MySQL.
- Git instalado.
- Dependências listadas em "requirements.txt".

Instalação

1. Clone o repositório

git clone https://github.com/Diogohk/IFPI---BIBLIOTECA.git

2. Acesse a pasta do projeto

cd "IFPI---BIBLIOTECA"

Caso os arquivos estejam em uma subpasta, acesse também essa pasta.

3. Crie um ambiente virtual

python -m venv venv

Ative o ambiente virtual:

Windows:

venv\Scripts\activate

Linux/macOS:

source venv/bin/activate

4. Instale as dependências

pip install -r requirements.txt

5. Configure o banco de dados

Inicie o MySQL pelo XAMPP e prepare o banco de dados conforme a configuração definida pela equipe.

A conexão deverá utilizar o driver PyMySQL e as credenciais do ambiente local.

Não compartilhe senhas ou credenciais no repositório.

6. Execute a aplicação

Após a implementação do ponto de entrada da aplicação:

python run.py

O endereço local será informado pelo Flask no terminal.

«Observação: os comandos de execução dependem da conclusão da estrutura de inicialização da aplicação.»

Desenvolvimento

O desenvolvimento está organizado em etapas:

1. Organização do ambiente e do repositório.
2. Definição e revisão da estrutura do banco de dados.
3. Configuração do Flask e SQLAlchemy.
4. Implementação dos modelos.
5. Desenvolvimento dos formulários.
6. Implementação das operações CRUD.
7. Testes e validações.
8. Documentação e preparação da entrega.

Equipe

Guardiões da Galáxia

- Diogo Luiz Reis Rufino
- Renan Silva Nascimento
- Brenno Ramos Cruz
- Hitallo Rodrigues de Alencar
- Kauan Ramos da Silva

Situação do projeto

O projeto encontra-se em desenvolvimento. A equipe está trabalhando na estruturação da aplicação, na integração com o banco de dados e na criação dos modelos de dados.

As funcionalidades serão documentadas e atualizadas conforme forem implementadas e testadas.

---

Desenvolvido no âmbito das atividades acadêmicas do IFPI — Campus Paulistana.
