# [Nome do Projeto]

<!-- Badges (opcional) -->
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

Esse projeto foi desenvolvido com o objetivo de obter conhecimentos iniciais sobre Engenharia de Dados através de um pipeline ETL que analisa a relação entre a pobreza e a falta de estrutura educacional no Brasil. Futuramente, serão adicionados dados referentes à criminalidade, permitindo uma visão mais ampla a respeito das vulnerabilidades sociais.

Para a criação desse pipeline, foram utilizadas três bases de dados públicas:

* **[Censo Escolar 2024](https://www.gov.br/inep/pt-br/acesso-a-informacao/dados-abertos/microdados/censo-escolar):** Microdados utilizados para extrair métricas de infraestrutura das escolas por município (acesso à água, energia, esgoto, internet, etc.).
* **[Cadastro Único 2024]():** Dados extraídos para contabilizar o volume de famílias em situação de pobreza e baixa renda.
* **[População Estimada 2024](https://sidra.ibge.gov.br/tabela/6579):** Dados demográficos consumidos via API SIDRA para cruzamento e proporção dos indicadores.

O ano de 2024 foi escolhido porque apresentou os dados mais completos e padronizados nas três plataformas simultaneamente. Essa consistência foi essencial para garantir um cruzamento confiável entre as bases e evitar informações em falta na análise final.

## 🏗️ Arquitetura
O fluxo de dados segue a arquitetura Medalhão e é orquestrado pelo Apache Airflow. Todo o ambiente de extração, Data Lake (MinIO) e Data Warehouse (PostgreSQL) está conteinerizado utilizando Docker.
<img width="1292" height="621" alt="Diagrama_Arquitetura" src="https://github.com/user-attachments/assets/ba17bea0-0af9-4ac4-89ec-ccb16b9720cb" />

## 💻 Tecnologias Utilizadas

- **[ ]**
- **[ ]**
- **[ ]**

## ⚙️ Pré-requisitos

[ ]

- [ ]
- [ ]

## 🚀 Instalação e Execução

### Passo 1: [ ]

```bash
# Comando de exemplo
```

### Passo 2: [ ]

```bash
# Comando de exemplo
```

## 📊 Modelagem de Dados

[ ]

<!-- Exemplo de tabela em Markdown -->
| Camada | Descrição |
| ------ | --------- |
| Bronze | [ ]       |
| Silver | [ ]       |
| Gold   | [ ]       |

## ✉️ Contato

- **[Seu Nome]** - [Seu Email]
- **LinkedIn**: [Link para o LinkedIn]
- **Portfólio/GitHub**: [Link para o GitHub]
