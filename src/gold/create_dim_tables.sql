

CREATE TABLE IF NOT EXISTS d_municipio (
    co_municipio INT PRIMARY KEY,
    nome_municipio VARCHAR(250) NOT NULL
)

CREATE TABLE IF NOT EXISTS d_regiao (
    id_regiao SERIAL PRIMARY KEY,
    nome_regiao VARCHAR(250) NOT NULL
)

CREATE TABLE IF NOT EXISTS d_uf (
    id_uf SERIAL PRIMARY KEY,
    sigla_uf VARCHAR(2) NOT NULL
)