Documentação Técnica — Biblioteca IFPI

Projeto: Sistema de Gerenciamento de Biblioteca
Equipe: Guardiões da Galáxia
Instituição: IFPI — Campus Paulistana
Data de referência: Novembro de 2026

---

1. Introdução

Este documento apresenta a documentação técnica do sistema Biblioteca IFPI, desenvolvido para auxiliar os funcionários do Setor de Biblioteca do IFPI — Campus Paulistana.

A aplicação tem como finalidade organizar informações relacionadas aos alunos, livros, exemplares, empréstimos e devoluções.

A documentação descreve os objetivos, tecnologias, organização da aplicação, estrutura de dados prevista, requisitos, cuidados de segurança e procedimentos de teste.

Como o sistema ainda está em desenvolvimento, os elementos não confirmados são identificados como planejados ou pendentes.

2. Objetivos do sistema

2.1 Objetivo geral

Desenvolver uma aplicação web que facilite o gerenciamento das atividades da biblioteca, tornando o armazenamento, a consulta e a atualização de informações mais organizados e eficientes.

2.2 Objetivos específicos

- Permitir o registro de alunos.
- Organizar as informações dos livros.
- Controlar os exemplares pertencentes ao acervo.
- Registrar empréstimos e devoluções.
- Facilitar a consulta dos registros.
- Reduzir inconsistências nos registros da biblioteca.
- Garantir maior organização e segurança dos dados.

3. Público-alvo

O público-alvo inicial são os funcionários do Setor de Biblioteca do IFPI — Campus Paulistana.

A possibilidade de disponibilizar funcionalidades diretamente aos alunos poderá ser considerada em futuras versões.

4. Tecnologias e ferramentas

4.1 Python

Linguagem utilizada no desenvolvimento do back-end da aplicação.

4.2 Flask

Framework responsável pelo funcionamento da aplicação web, gerenciamento de rotas e comunicação entre o servidor e as páginas.

4.3 SQLAlchemy

ORM (Object-Relational Mapping) utilizado para representar as tabelas do banco de dados por meio de classes Python.

Isso permite realizar operações de persistência utilizando objetos, sem depender da escrita manual de SQL para cada operação.

4.4 Flask-SQLAlchemy

Extensão que integra o SQLAlchemy ao Flask, facilitando a configuração e o gerenciamento da conexão com o banco.

4.5 MySQL

Banco de dados relacional responsável pelo armazenamento das informações.

4.6 PyMySQL

Driver utilizado para permitir a comunicação entre Python e MySQL.

4.7 HTML, CSS e JavaScript

Tecnologias utilizadas na construção da interface:

- HTML: estrutura dos formulários e páginas.
- CSS: apresentação visual.
- JavaScript: interações e validações no navegador.

4.8 Requests e Google Books

A biblioteca Requests poderá ser utilizada para realizar requisições HTTP à API pública do Google Books, auxiliando na busca de informações bibliográficas.

Essa integração é complementar ao funcionamento principal do sistema.

5. Arquitetura da aplicação

A aplicação segue uma organização baseada na separação de responsabilidades.

5.1 Camada de apresentação

Responsável pela interface exibida ao funcionário.

Tecnologias:

- HTML;
- CSS;
- JavaScript;
- Templates do Flask.

5.2 Camada de aplicação

Responsável pelo processamento das requisições e execução das regras de negócio.

Tecnologia principal:

- Flask.

5.3 Camada de persistência

Responsável pela comunicação com o banco de dados e pelas operações de armazenamento e consulta.

Tecnologias:

- Flask-SQLAlchemy;
- SQLAlchemy;
- PyMySQL;
- MySQL.

5.4 Fluxo de funcionamento

O fluxo geral planejado é:

1. O funcionário acessa uma página do sistema.
2. O navegador apresenta o formulário correspondente.
3. O funcionário informa os dados.
4. O Flask recebe e processa a requisição.
5. Os dados são validados no servidor.
6. O SQLAlchemy executa a operação necessária.
7. O MySQL armazena ou fornece as informações.
8. O sistema apresenta uma resposta ao funcionário.

6. Organização dos arquivos

A estrutura modular proposta é:

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

Responsabilidade de cada componente

Arquivo/pasta| Responsabilidade
"app/"| Reunir os componentes da aplicação
"__init__.py"| Inicialização e configuração da aplicação
"config.py"| Configurações do sistema
"extensions.py"| Instâncias das extensões utilizadas
"models/"| Classes que representam as tabelas
"routes/"| Rotas e processamento das requisições
"templates/"| Páginas HTML
"static/css/"| Arquivos de estilização
"static/js/"| Scripts JavaScript
"static/img/"| Imagens utilizadas na interface
".env"| Configurações sensíveis do ambiente, caso seja adotado
".gitignore"| Arquivos que não devem ser enviados ao Git
"requirements.txt"| Dependências Python
"run.py"| Ponto de entrada para execução

A estrutura ainda deverá ser confrontada com os arquivos efetivamente implementados.

7. Modelagem do banco de dados

A modelagem definitiva deverá seguir o diagrama elaborado por Brenno e aprovado pela equipe.

O escopo funcional contempla os seguintes conceitos:

- Alunos;
- Livros ou títulos;
- Exemplares;
- Empréstimos;
- Devoluções.

É importante distinguir livro e exemplar: um título pode possuir vários exemplares físicos. A representação definitiva dessa relação depende da aprovação do diagrama.

7.1 Modelos SQLAlchemy

Os modelos são classes Python que representam entidades armazenadas no banco de dados.

Como exemplo do trabalho iniciado, a estrutura do modelo Aluno utiliza:

- Identificador;
- Nome;
- Matrícula;
- E-mail.

O modelo deve utilizar a classe-base "db.Model" e definir suas colunas com "db.Column".

Exemplo conceitual:

class Aluno(db.Model):
    __tablename__ = "alunos"

    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    matricula = db.Column(db.String(20), unique=True)
    email = db.Column(db.String(120))

Este trecho é ilustrativo. Os tipos, tamanhos, restrições e campos definitivos devem ser conferidos com o modelo aprovado pela equipe e com o código atual.

7.2 Chaves e relacionamentos

A modelagem deverá definir:

- Chaves primárias (PK): identificam cada registro.
- Chaves estrangeiras (FK): estabelecem referências entre tabelas.
- Cardinalidades: definem quantos registros podem estar relacionados.

Nenhuma chave estrangeira ou cardinalidade deverá ser definida sem conferir o diagrama aprovado.

8. Requisitos funcionais

Código| Requisito
RF01| Permitir cadastrar alunos.
RF02| Permitir consultar alunos.
RF03| Permitir editar informações de alunos.
RF04| Permitir excluir registros de alunos.
RF05| Permitir cadastrar livros.
RF06| Permitir consultar livros.
RF07| Permitir gerenciar exemplares.
RF08| Permitir registrar empréstimos.
RF09| Permitir registrar devoluções.

Esses requisitos representam o escopo funcional planejado. Sua implementação deverá ser confirmada individualmente.

9. Requisitos não funcionais

Código| Requisito
RNF01| A aplicação deverá ser desenvolvida utilizando Python e Flask.
RNF02| Os dados deverão ser armazenados em um banco de dados relacional MySQL.
RNF03| A persistência deverá utilizar SQLAlchemy/ORM.
RNF04| A interface deverá ser acessível por navegador web.
RNF05| Os dados recebidos deverão passar por validação no servidor.
RNF06| Credenciais e informações sensíveis não deverão ser expostas no repositório.
RNF07| O conteúdo fornecido pelos usuários deverá ser tratado de forma segura.

10. Segurança e validação

A aplicação deverá adotar cuidados para proteger os dados e evitar operações indevidas.

10.1 Validação de dados

Os formulários deverão verificar se os dados enviados atendem às regras estabelecidas.

Exemplos:

- Campos obrigatórios preenchidos.
- Formatos válidos.
- Matrículas únicas, quando exigido.
- Referências válidas a registros relacionados.

A validação deverá acontecer também no servidor, não somente no navegador.

10.2 Proteção CSRF

Formulários que alteram informações deverão contar com proteção contra ataques CSRF.

A utilização de Flask-WTF ou outra solução compatível deverá ser confirmada na implementação.

10.3 Escape de conteúdo

Textos fornecidos pelos usuários deverão ser tratados corretamente antes de serem exibidos nas páginas, evitando que conteúdo seja interpretado indevidamente como HTML ou JavaScript.

10.4 Uso do ORM

As operações de banco deverão utilizar SQLAlchemy para reduzir a necessidade de consultas SQL construídas manualmente e facilitar o tratamento dos dados.

10.5 Proteção de credenciais

Senhas e informações de conexão não deverão ser armazenadas diretamente no código-fonte ou publicadas no GitHub.

11. Formulários previstos

Para atender ao planejamento do Marco 4+5, foram considerados três formulários iniciais:

1. Cadastro de aluno.
2. Cadastro de livro.
3. Cadastro de exemplar.

Cada formulário deverá apresentar:

- Campos de entrada;
- Validação;
- Mensagens de retorno;
- Processamento pelo Flask;
- Persistência no banco;
- Consulta ou conferência dos dados cadastrados.

A seleção definitiva dos formulários deverá ser confirmada pela equipe.

12. Operações CRUD

CRUD representa quatro operações fundamentais:

Operação| Significado| Exemplo
Create| Criar| Cadastrar aluno
Read| Ler| Consultar aluno
Update| Atualizar| Editar cadastro
Delete| Excluir| Remover cadastro

O Marco 4+5 exige que as quatro operações funcionem em pelo menos duas tabelas relacionadas.

A equipe deverá demonstrar essas operações utilizando os dados efetivamente armazenados no MySQL.

13. Plano de testes

A aplicação deverá possuir uma tabela de testes com pelo menos cinco casos.

Exemplo de planejamento:

Teste| Cenário| Resultado esperado
T01| Cadastrar aluno com dados válidos| Registro salvo corretamente
T02| Enviar formulário com campo obrigatório vazio| Sistema informa a validação
T03| Cadastrar matrícula duplicada| Sistema impede a duplicidade
T04| Consultar aluno cadastrado| Sistema apresenta os dados
T05| Editar informações de aluno| Sistema atualiza o registro
T06| Excluir registro permitido| Sistema remove o registro
T07| Enviar referência inexistente| Sistema rejeita a operação

A tabela final deverá conter também o resultado obtido em cada teste, identificando se foi aprovado ou reprovado.

14. Etapas de desenvolvimento

A sequência de trabalho prevista é:

1. Revisão do diagrama de classes.
2. Definição das tabelas e relacionamentos.
3. Preparação do ambiente Python.
4. Configuração do Flask e SQLAlchemy.
5. Implementação dos modelos.
6. Desenvolvimento dos formulários.
7. Integração com MySQL.
8. Implementação das operações CRUD.
9. Testes e correções.
10. Atualização da documentação.
11. Preparação das evidências e apresentação.
12. Hospedagem da aplicação.

15. Cronograma acadêmico

Conforme o planejamento da disciplina:

Marco| Atividade
Marco 4+5| Formulários, segurança, CRUD, banco de dados, testes e documentação
Marco 6| Hospedagem
Marco 7| Apresentação final do projeto completo

Data prevista para a entrega do Marco 4+5: 26/11/2026.

16. Evidências da implementação

Para a entrega acadêmica, deverão ser reunidas evidências do funcionamento do sistema:

- Formulários implementados;
- Conferência dos dados na tela;
- Mensagens de validação e erro;
- Diagrama atualizado;
- Banco de dados com registros;
- Demonstração de cadastro e consulta;
- Demonstração de edição e exclusão;
- Tabela de testes preenchida;
- Histórico de commits;
- Participação dos integrantes na apresentação.

17. Equipe de desenvolvimento

Guardiões da Galáxia

- Diogo Luiz Reis Rufino
- Renan Silva Nascimento
- Brenno Ramos Cruz
- Hitallo Rodrigues de Alencar
- Kauan Ramos da Silva

A distribuição definitiva das responsabilidades técnicas deverá ser mantida atualizada conforme as decisões da equipe.

18. Pendências e atualizações

Os seguintes pontos ainda precisam ser confirmados ou concluídos:

- [ ] Revisar e aprovar o diagrama de classes.
- [ ] Confirmar tabelas, atributos e relacionamentos.
- [ ] Finalizar os modelos SQLAlchemy.
- [ ] Confirmar os três formulários.
- [ ] Implementar as operações CRUD em duas tabelas relacionadas.
- [ ] Configurar e validar a conexão com MySQL.
- [ ] Implementar proteção CSRF.
- [ ] Confirmar configuração por variáveis de ambiente.
- [ ] Preencher a tabela de testes com resultados reais.
- [ ] Atualizar o diagrama conforme o banco implementado.
- [ ] Reunir os prints de funcionamento.

Regra de manutenção: esta documentação deverá ser atualizada sempre que uma funcionalidade for implementada, uma decisão técnica for aprovada ou a estrutura do projeto sofrer alterações.

Não considerar uma funcionalidade concluída apenas porque foi planejada ou documentada.
