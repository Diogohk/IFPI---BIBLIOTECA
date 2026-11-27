# Biblioteca IFPI — Sistema de Gerenciamento

**Equipe:** Guardiões da Galáxia  
**Instituição:** Instituto Federal do Piauí (IFPI) — Campus Paulistana

## Sobre o projeto

O Biblioteca IFPI é um sistema web desenvolvido para apoiar as atividades do Setor de Biblioteca do IFPI — Campus Paulistana. A aplicação é direcionada aos funcionários da biblioteca e oferece cadastro e consulta de livros em formato de catálogo, cadastro, consulta e edição de alunos, além de pesquisa de metadados bibliográficos pela API Google Books.

O projeto está em desenvolvimento. Funcionalidades que ainda não estejam integradas e testadas — como cadastro de exemplares, empréstimos, devoluções, movimentações e estatísticas — não devem ser consideradas disponíveis.

## Tecnologias

- Python 3.10 ou superior
- Flask
- Flask-SQLAlchemy e SQLAlchemy (ORM)
- MySQL e PyMySQL
- Flask-WTF (proteção CSRF)
- HTML, CSS e JavaScript
- Google Books API (pesquisa de metadados e seleção de capas)
- XAMPP (opção para executar o MySQL localmente)

## Requisitos

Antes de começar, instale Python 3.10 ou superior, Git, MySQL (ou XAMPP) e um editor de código.

## Instalação

Clone o repositório:

```bash
git clone https://github.com/Diogohk/IFPI---BIBLIOTECA.git
cd "IFPI---BIBLIOTECA/BIBLIOTECA - PROJETO"
```

No Windows, crie e ative o ambiente virtual:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

Instale as dependências:

```bash
python -m pip install --upgrade pip
pip install -r requirements.txt
```

## Configuração do banco de dados e APIs

1. Inicie o serviço MySQL.
2. Copie `.env.example` para `.env`.
3. Preencha `DB_USER`, `DB_PASSWORD`, `DB_HOST` e `DB_NAME`.
4. Defina uma `SECRET_KEY` privada e aleatória.
5. Habilite a Books API no Google Cloud e configure `GOOGLE_BOOKS_API_KEY` no `.env`.
6. Nunca publique o arquivo `.env`, senhas ou chaves no GitHub.

A consulta ao Google Books é feita pelo back-end Flask, pela rota autenticada `/api/google-books`. A chave da API não é enviada ao navegador.

### Migração para salvar a capa selecionada

O sistema salva no cadastro o endereço da capa escolhida na pesquisa do Google Books. Para bancos já existentes, faça backup e execute uma única vez o script `MIGRACAO_CAPA_LIVRO.sql` no banco da biblioteca:

```sql
ALTER TABLE livros ADD COLUMN capa_url TEXT NULL;
```

O campo novo não é criado automaticamente por `db.create_all()` em tabelas existentes. Se a coluna `capa_url` já existir, não execute a migração novamente.

## Como executar

Com o ambiente virtual ativado e o MySQL em execução:

```bash
python run.py
```

Abra o endereço informado no terminal, normalmente `http://127.0.0.1:5000`.

## Acesso de funcionário

O sistema é destinado aos funcionários da biblioteca. Cadastre o primeiro funcionário executando, na pasta do projeto:

```bash
python criar_funcionario.py
```

O script solicita matrícula, nome, cargo e senha. A senha é armazenada como hash. Depois, entre pela tela `/login`.

## Arquivos importantes

| Arquivo ou pasta | Finalidade |
|---|---|
| `app/` | Código da aplicação Flask |
| `.env.example` | Exemplo das configurações de ambiente |
| `criar_funcionario.py` | Cadastro inicial de funcionário |
| `MIGRACAO_MARCO_4_5.sql` | Migração anterior de ISBN e código de exemplar |
| `MIGRACAO_CAPA_LIVRO.sql` | Adiciona o campo para persistir a capa escolhida |
| `requirements.txt` | Dependências Python |
| `run.py` | Inicialização da aplicação |

## Segurança

- Não envie credenciais, senhas ou o arquivo `.env` para o repositório.
- Mantenha uma `SECRET_KEY` privada e aleatória.
- As senhas dos funcionários são armazenadas como hash.
- A URL da capa recebida do formulário é validada para aceitar somente HTTPS nos domínios de imagens do Google Books.

## Situação do desenvolvimento

O projeto está em desenvolvimento. Consulte a aplicação e a documentação atualizadas para identificar quais funcionalidades estão implementadas e testadas.

## Equipe

**Guardiões da Galáxia**  
Instituto Federal do Piauí (IFPI) — Campus Paulistana
