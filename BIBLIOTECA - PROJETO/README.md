# Biblioteca IFPI — Sistema de Gerenciamento

**Equipe:** Guardiões da Galáxia  
**Instituição:** Instituto Federal do Piauí (IFPI) — Campus Paulistana

## Sobre o projeto

O Biblioteca IFPI é um sistema web desenvolvido para apoiar as atividades do Setor de Biblioteca do IFPI — Campus Paulistana. A aplicação é direcionada aos funcionários da biblioteca e permite, na etapa atual, acessar os formulários de cadastro de livros e alunos e consultar os alunos cadastrados.

O projeto está em desenvolvimento. Funcionalidades ainda não integradas, como cadastro de exemplares, empréstimos, devoluções, movimentações e estatísticas, não devem ser consideradas disponíveis.

## Tecnologias

- Python e Flask
- Flask-SQLAlchemy e SQLAlchemy (ORM)
- MySQL e PyMySQL
- Flask-WTF (proteção CSRF)
- HTML, CSS e JavaScript
- XAMPP (opção para executar o MySQL localmente)

## Requisitos

- Python 3.10 ou superior
- MySQL em execução (pode ser iniciado pelo XAMPP)
- Git
- Dependências de `requirements.txt`

## Como instalar e executar

### 1. Baixar o projeto

```bash
git clone https://github.com/Diogohk/IFPI---BIBLIOTECA.git
cd IFPI---BIBLIOTECA/"BIBLIOTECA - PROJETO"
```

### 2. Criar e ativar o ambiente virtual

```bash
python -m venv venv
```

Windows:

```bash
venv\Scripts\activate
```

Linux/macOS:

```bash
source venv/bin/activate
```

### 3. Instalar as dependências

```bash
pip install -r requirements.txt
```

### 4. Preparar o banco de dados

1. Inicie o serviço MySQL pelo XAMPP ou por outro gerenciador.
2. Abra o phpMyAdmin (ou outro cliente MySQL).
3. Crie um banco de dados chamado `biblioteca`, utilizando codificação `utf8mb4`.

Se optar por executar o comando SQL:

```sql
CREATE DATABASE biblioteca CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
```

### 5. Configurar as variáveis de ambiente

Crie uma cópia de `.env.example` com o nome `.env`, na pasta `BIBLIOTECA - PROJETO`.

Preencha os dados de acesso ao MySQL. Exemplo para uma instalação local do XAMPP:

```env
SECRET_KEY=coloque_uma_chave_aleatoria
DB_USER=root
DB_PASSWORD=
DB_HOST=localhost
DB_NAME=biblioteca
```

Gere uma chave secreta própria e substitua o valor de exemplo. Uma opção é executar:

```bash
python -c "import secrets; print(secrets.token_hex(32))"
```

Não publique o arquivo `.env` nem compartilhe suas credenciais. Ele já está listado no `.gitignore`.

### 6. Criar o primeiro funcionário (primeiro acesso)

**Antes de abrir a tela de login, é necessário cadastrar pelo menos um funcionário.** O sistema não cria uma conta padrão.

Com o MySQL ligado e o arquivo `.env` configurado, execute:

```bash
python criar_funcionario.py
```

O programa solicitará matrícula, nome, cargo e senha. A senha é digitada sem aparecer no terminal, precisa ter pelo menos oito caracteres e é armazenada no banco usando hash seguro do Werkzeug. O programa também cria as tabelas mapeadas pela aplicação, caso ainda não existam.

Guarde a matrícula e a senha informadas: elas serão usadas na tela de login. Para cadastrar outro funcionário, execute o mesmo comando novamente com uma matrícula diferente.

### 7. Iniciar o sistema

```bash
python run.py
```

Abra no navegador o endereço local exibido no terminal (normalmente http://127.0.0.1:5000) e entre com a matrícula e a senha cadastradas no passo anterior.

## Estrutura principal

```text
BIBLIOTECA - PROJETO/
├── app/
│   ├── models/
│   ├── routes/
│   ├── static/
│   └── templates/
├── .env.example
├── criar_funcionario.py
├── requirements.txt
└── run.py
```

## Segurança

- As senhas dos funcionários são armazenadas como hash, nunca em texto puro.
- Os formulários que alteram dados utilizam proteção CSRF.
- As credenciais locais ficam no arquivo `.env`, que não deve ser enviado ao GitHub.
- O cadastro inicial é feito localmente pelo script `criar_funcionario.py`; não existe usuário ou senha padrão no repositório.

## Funcionalidades na etapa atual

- Login de funcionário.
- Cadastro de livros (formulário e rota existentes; a integração de gravação deve ser conferida conforme a etapa de desenvolvimento).
- Cadastro de alunos.
- Consulta/listagem de alunos.

Cadastro de exemplares, empréstimos, devoluções, movimentações e estatísticas permanecem como etapas futuras ou em integração.

## Equipe

Guardiões da Galáxia — IFPI, Campus Paulistana.

---
Desenvolvido no âmbito das atividades acadêmicas do IFPI — Campus Paulistana.
