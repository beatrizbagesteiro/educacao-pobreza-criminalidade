# Pipeline de Dados Educacionais e Socioeconômicos (Brasil - 2024)

![Status](https://img.shields.io/badge/status-em%20desenvolvimento-green)

## 📋 Índice

- [Sobre o Projeto](#-sobre-o-projeto)
- [Arquitetura](#-arquitetura)
- [Tecnologias Utilizadas](#-tecnologias-utilizadas)
- [Pré-requisitos](#-pré-requisitos)
- [Instalação e Execução](#-instalação-e-execução)
- [Modelagem de Dados](#-modelagem-de-dados)
- [Contato](#-contato)

---

## 📖 Sobre o Projeto

Esse projeto foi desenvolvido para consolidar conhecimentos iniciais em Engenharia de Dados através de um pipeline que prepara os dados para uma análise futura sobre a relação entre a pobreza e a falta de estrutura educacional no Brasil. Futuramente, serão adicionados dados referentes à criminalidade, permitindo uma visão mais ampla a respeito das vulnerabilidades sociais.

Para a criação desse pipeline, foram utilizadas três bases de dados públicas:

* **[Censo Escolar 2024](https://www.gov.br/inep/pt-br/acesso-a-informacao/dados-abertos/microdados/censo-escolar):** Microdados utilizados para extrair métricas de infraestrutura das escolas por município (acesso à água, energia, esgoto, internet, etc.).
* **[Cadastro Único 2024]():** Dados extraídos para contabilizar o volume de famílias em situação de pobreza e baixa renda.
* **[População Estimada 2024](https://sidra.ibge.gov.br/tabela/6579):** Dados demográficos consumidos via API SIDRA para cruzamento e proporção dos indicadores.

O ano de 2024 foi escolhido porque apresentou os dados mais completos e padronizados nas três plataformas simultaneamente. Essa consistência foi essencial para garantir um cruzamento confiável entre as bases e evitar informações em falta na análise final.

## 🏗️ Arquitetura
O fluxo de dados segue a arquitetura Medalhão e é orquestrado pelo Apache Airflow. Todo o ambiente de extração, Data Lake (MinIO) e Data Warehouse (PostgreSQL) está conteinerizado utilizando Docker.

<img width="1292" height="620" alt="Diagrama_Arquitetura" src="https://github.com/user-attachments/assets/89531699-833a-411c-9ddc-6d5ce62a9bf8" />

## 💻 Tecnologias Utilizadas

- **Python**
- **Pandas**
- **Apache Airflow**
- **MinIO**
- **PostgreSQL**
- **Docker & Docker Compose**

## ⚙️ Pré-requisitos
- **Git**: Para clonar o repositório.
- **Docker e Docker Compose**: Para orquestrar os serviços da arquitetura (Airflow, MinIO e PostgreSQL).

## 🚀 Instalação e Execução

### Passo 1
```bash
git clone https://github.com/beatrizbagesteiro/educacao-pobreza-criminalidade.git
```

### Passo 2
Inicie os contêineres do Airflow, MinIO e PostgreSQL através do comando abaixo:
```bash
docker compose up -d
```

### Passo 3
As ferramentas estarão disponíveis localmente:
- Apache Airflow: http://localhost:8080 
- MinIO Console: http://localhost:9001 
- PostgreSQL: Conecte via interface de sua preferência ou por linha de comando.
  
## 📊 Modelagem de Dados
O projeto segue a Arquitetura Medalhão para estruturar o fluxo de dados em três níveis progressivos de refinamento:

| Camada | Descrição |
| ------ | --------- |
| Bronze | Armazenamento dos dados brutos no MinIO, preservando o histórico original extraído das fontes (INEP, CadÚnico e IBGE SIDRA) sem qualquer alteração.       |
| Silver | Limpeza, padronização de tipos e conversão dos dados para o formato Parquet no MinIO, seguidos pela ingestão em uma área de *staging* temporária no PostgreSQL.       |
| Gold   | Modelagem dimensional (*Star Schema*) no PostgreSQL, organizando os dados consolidados em tabelas Fato e Dimensão totalmente prontas para consumo analítico e ferramentas de BI.       |

## 🚀 To do
Alterações futuras:
* **Ingestão de um novo DataSet:** Ingestão e modelagem de conjuntos de dados governamentais de Segurança Pública (Criminalidade).
* **Visualização de Dados e BI:** Conexão da camada Gold do PostgreSQL com uma ferramenta de Business Intelligence.

## ✉️ Contato

- **Beatriz Pimentel Bagesteiro Alves** - beatriz_bagesteiro@hotmail.com
- **LinkedIn**: [Link para o LinkedIn](https://www.linkedin.com/in/beatriz-p-b-alves/)
