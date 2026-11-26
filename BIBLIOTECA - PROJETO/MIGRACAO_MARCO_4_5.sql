-- Execute uma única vez no banco biblioteca já existente.
-- Faça backup antes de alterar tabelas em uso.

ALTER TABLE livros
    ADD COLUMN isbn VARCHAR(17) NULL,
    ADD UNIQUE KEY uq_livros_isbn (isbn);

ALTER TABLE exemplares
    ADD COLUMN codigo VARCHAR(30) NULL;

-- Os códigos antigos recebem identificadores derivados da chave já existente.
UPDATE exemplares
SET codigo = CONCAT('EX-', idexemplar)
WHERE codigo IS NULL OR codigo = '';

ALTER TABLE exemplares
    MODIFY codigo VARCHAR(30) NOT NULL,
    ADD UNIQUE KEY uq_exemplares_codigo (codigo);
