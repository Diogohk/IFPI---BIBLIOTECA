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
- Google Books API (pesquisa de metadados e capas de livros)
- XAMPP (opção para executar o MySQL localmente)

## Requisitos

Antes de começar, instale:

- Python 3.10 ou superior
- Git
- MySQL (pode ser iniciado pelo XAMPP)
- Visual Studio Code ou outro editor de sua preferência

## Instalação

### 1. Baixar o projeto

Abra o terminal e execute:

```bash
git clone https://github.com/Diogohk/IFPI---BIBLIOTECA.git
```

Entre na pasta do projeto:

```bash
cd "IFPI---BIBLIOTECA/BIBLIOTECA - PROJETO"
```

Se o nome ou a organização das pastas no seu computador estiver diferente, entre na pasta `BIBLIOTECA - PROJETO` antes de continuar.

### 2. Criar e ativar o ambiente virtual

No Windows, dentro da pasta `BIBLIOTECA - PROJETO`, execute:

```powershell
python -m venv .venv
```

Ative o ambiente virtual:

```powershell
.\.venv\Scripts\Activate.ps1
```

Se o PowerShell bloquear a ativação, abra o terminal Prompt de Comando (cmd) no VS Code e use:

```bat
.venv\Scripts\activate.bat
```

### 3. Instalar as dependências

Com o ambiente virtual ativado, execute:

```bash
python -m pip install --upgrade pip
pip install -r requirements.txt
```

## Configuração do banco de dados

1. Inicie o serviço MySQL. Se estiver usando XAMPP, abra o painel do XAMPP e inicie o MySQL.
2. Na pasta principal do projeto, localize o arquivo `.env.example`.
3. Crie uma cópia desse arquivo com o nome `.env`.
4. Preencha no `.env` os dados de conexão com o MySQL. As variáveis utilizadas são `DB_USER`, `DB_PASSWORD`, `DB_HOST` e `DB_NAME`.
5. Defina também uma `SECRET_KEY` privada e aleatória. Não utilize a chave de exemplo em produção.
6. Crie uma chave no Google Cloud com a **Books API** habilitada e coloque-a na variável `GOOGLE_BOOKS_API_KEY` do arquivo `.env`.
7. Nunca publique o arquivo `.env`, senhas ou outras credenciais no GitHub.

A consulta ao Google Books é feita pelo back-end Flask, que lê `GOOGLE_BOOKS_API_KEY` do ambiente. O navegador chama apenas a rota autenticada `/api/google-books`, portanto a chave não é exposta no JavaScript. Como a chamada é feita pelo servidor, não use restrição de aplicativo por HTTP referrer. Em desenvolvimento local, deixe a restrição de aplicativo sem restrição e mantenha a restrição de API limitada à Books API. Em produção, prefira também restringir pelo IP fixo de saída do servidor, quando disponível.

O projeto utiliza SQLAlchemy. Na inicialização, a aplicação chama `db.create_all()` para criar tabelas ausentes e executa as migrações automáticas definidas em `app/migrations.py`. O `db.create_all()` isoladamente **não altera a estrutura de tabelas já existentes**; por isso, alterações de esquema precisam de migrações explícitas.

Se o banco já possuir tabelas de versões anteriores, consulte os scripts de migração antes de iniciar:

- `MIGRACAO_MARCO_4_5.sql`: adiciona os campos de ISBN aos livros e código aos exemplares. Faça backup do banco e confira se a migração ainda precisa ser aplicada antes de executá-la.
- `CONFIGURAR_ACESSO.md`: orienta a configuração das colunas de matrícula e hash de senha na tabela de funcionários. Siga as instruções com atenção, especialmente se já existirem funcionários cadastrados.

Não execute migrações repetidamente: os comandos de alteração de estrutura devem ser aplicados conforme o estado atual do banco.



### Capas dos livros no catálogo

Ao selecionar um resultado na pesquisa do Google Books, o formulário também salva o endereço da capa escolhida. O catálogo exibe essa capa salva e não faz uma nova pesquisa por ISBN. A capa pode ser escolhida tanto no cadastro quanto na edição de um livro.

A coluna `capa_url` é verificada e criada automaticamente pela aplicação na inicialização, por meio de `app/migrations.py`. Assim, ao atualizar o projeto e iniciar com `python run.py`, bancos antigos recebem a coluna sem precisar executar SQL manualmente. A rotina verifica se a coluna já existe e não a duplica. O arquivo `MIGRACAO_CAPA_LIVRO.sql` fica disponível apenas como referência para recuperação manual em instalações antigas nas quais a inicialização automática não possa ser utilizada. Faça backup antes de qualquer alteração manual.

## Como executar

Com o ambiente virtual ativado, o MySQL em execução e o banco configurado, execute na pasta principal:

```bash
python run.py
```

Depois, observe o endereço informado no terminal e abra-o no navegador. Na configuração padrão do Flask, o endereço local costuma ser:

```
http://127.0.0.1:5000
```

Se ocorrer um erro, confira primeiro se o MySQL está iniciado, se o arquivo `.env` está preenchido corretamente e se as dependências foram instaladas.

## Acesso de funcionário

O sistema é destinado aos funcionários da biblioteca. Não existe usuário ou senha padrão confirmada no projeto. É necessário cadastrar um funcionário antes de entrar.

### Criar o primeiro funcionário

Com o ambiente virtual ativado, o banco configurado e a partir da pasta `BIBLIOTECA - PROJETO`, execute:

```bash
python criar_funcionario.py
```

O script solicitará:

- Matrícula (até 20 caracteres, obrigatória e única)
- Nome completo (até 150 caracteres)
- Cargo (até 80 caracteres)
- Senha e confirmação da senha (mínimo de 8 caracteres)

A senha é solicitada sem aparecer na tela e armazenada no banco como hash. Guarde a senha em local seguro. O script também verifica se a matrícula já está cadastrada. Se ainda não houver administrador, o primeiro funcionário criado recebe essa permissão automaticamente.

Depois do cadastro, acesse a tela de login em `/login` e entre utilizando a matrícula e a senha criadas.

### Gestão de funcionários

Após entrar com uma conta administradora, use **Funcionários** no menu lateral para cadastrar, consultar, editar e excluir acessos. Contas novas recebem permissão de funcionário; somente um administrador pode gerenciar a equipe. O sistema impede excluir a própria conta e mantém pelo menos um administrador.

Cada funcionário pode acessar **Meu perfil** para atualizar nome, cargo e foto. As fotos aceitas são JPG, PNG e WEBP, com limite de 2 MB, armazenadas na pasta local `instance/uploads/funcionarios`, que não deve ser enviada ao GitHub.

Em bancos antigos, a inicialização adiciona automaticamente os campos de foto e permissão. Se já existirem funcionários e nenhum administrador, o cadastro mais antigo recebe a permissão inicial. Após atualizar o projeto, encerre a sessão e entre novamente para carregar as novas permissões.

### Modo escuro

O botão **Modo escuro**, no rodapé do menu lateral do painel, alterna a aparência do sistema. A preferência fica salva no navegador utilizado e não exige alteração no banco de dados.

Se houver dúvidas sobre a estrutura da tabela de funcionários ou se o banco já possuir registros, consulte primeiro `CONFIGURAR_ACESSO.md`. Não compartilhe credenciais de funcionários.

## Arquivos importantes

| Arquivo ou pasta | Finalidade |
|---|---|
| `app/` | Código da aplicação Flask |
| `.env.example` | Exemplo das configurações de ambiente |
| `.gitignore` | Arquivos que não devem ser enviados ao Git |
| `CONFIGURAR_ACESSO.md` | Orientações relacionadas à configuração do acesso |
| `criar_funcionario.py` | Script para cadastrar um funcionário |
| `MIGRACAO_MARCO_4_5.sql` | Script SQL de migração do banco |
| `requirements.txt` | Dependências Python |
| `run.py` | Arquivo de inicialização da aplicação |
| `test_connection.py` | Script de teste da conexão |

## Segurança

- Não envie credenciais, senhas ou o arquivo `.env` para o repositório.
- Mantenha o `.env` protegido e confira se ele está listado no `.gitignore`.
- Defina uma `SECRET_KEY` privada e aleatória fora do ambiente de desenvolvimento. A chave de fallback existente na configuração serve apenas para desenvolvimento e não deve ser usada em produção.
- As senhas dos funcionários são armazenadas como hash, não em texto puro.
- Utilize os formulários da aplicação e suas validações.
- As operações com o banco devem seguir a implementação baseada em SQLAlchemy/ORM.
- Não compartilhe credenciais de funcionários.

## Situação do desenvolvimento

O projeto está em desenvolvimento. Consulte a aplicação e a documentação atualizadas para identificar quais funcionalidades estão implementadas e testadas.

## Equipe

**Guardiões da Galáxia**  
Instituto Federal do Piauí (IFPI) — Campus Paulistana
