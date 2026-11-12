# Configuração inicial do acesso

O login exige funcionário previamente cadastrado, com matrícula única e senha armazenada como hash. Não há usuário ou senha padrão.

## Banco de dados

Faça backup do banco antes de alterar a tabela. Para uma tabela funcionarios ainda vazia, execute no MySQL:

```sql
ALTER TABLE funcionarios
  ADD COLUMN matricula VARCHAR(20) NOT NULL UNIQUE,
  ADD COLUMN senha_hash VARCHAR(255) NOT NULL;
```

Se já houver funcionários cadastrados, não execute esse comando diretamente: preencha matrículas e hashes para os registros existentes, em etapas, antes de aplicar NOT NULL e UNIQUE.

## Gerar hash de senha

No terminal, com o ambiente virtual ativado:

```bash
python -c "from werkzeug.security import generate_password_hash; print(generate_password_hash('SUA_SENHA_TEMPORARIA'))"
```

Cadastre o hash gerado na coluna senha_hash do funcionário. Nunca armazene senha em texto puro.

## Chave da aplicação

Crie o arquivo .env a partir do .env.example e defina uma SECRET_KEY aleatória e privada, além das credenciais do MySQL. Não publique o .env.

Depois execute `python run.py` e abra `http://127.0.0.1:5000/login`.
