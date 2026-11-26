-- Execute uma única vez no banco biblioteca já existente.
-- Faça backup antes de alterar tabelas em uso.
ALTER TABLE livros
    ADD COLUMN isbn VARCHAR(17) NULL,
    ADD UNIQUE KEY uq_livros_isbn (isbn);

ALTER TABLE exemplares
    ADD COLUMN codigo VARCHAR(30) NULL;

-- Preencha códigos únicos para exemplares já cadastrados antes de tornar
-- a coluna obrigatória. Exemplo (ajuste conforme os registros existentes):
-- UPDATE exemplares SET codigo = CONCAT('EX-', idexemplar) WHERE codigo IS NULL;

ALTER TABLE exemplares
    ADD UNIQUE KEY uq_exemplares_codigo (codigo);
-- Depois de preencher todos os códigos:
-- ALTER TABLE exemplares MODIFY codigo VARCHAR(30) NOT NULL;
