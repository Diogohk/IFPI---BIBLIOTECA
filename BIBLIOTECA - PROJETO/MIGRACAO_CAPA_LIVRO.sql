-- Execute uma única vez no banco de dados da Biblioteca IFPI.
-- Faça backup antes de alterar a estrutura.
ALTER TABLE livros ADD COLUMN capa_url TEXT NULL;
