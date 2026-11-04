CREATE TABLE IF NOT EXISTS gold.d_municipio (
    co_municipio INT PRIMARY KEY,
    no_municipio VARCHAR(250) NOT NULL,
    no_regiao VARCHAR(250),
    sg_uf VARCHAR(2),
    populacao INT
);

INSERT INTO gold.d_municipio (co_municipio, no_municipio, no_regiao, sg_uf, populacao)
SELECT 
    p.co_municipio,
    p.no_municipio,
    c.no_regiao,
    c.sg_uf,
    p.cont_populacao
FROM 
    silver.populacao_estimada_2024 p
LEFT JOIN (
    SELECT DISTINCT co_municipio, no_regiao, sg_uf
    FROM silver.censo_escolar_2024 
) c on p.co_municipio = c.co_municipio;


