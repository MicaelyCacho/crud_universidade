# Sistema Academico - Parte 1

Este projeto consiste em um sistema em Python para gerenciar operacoes de CRUD (Create, Read, Update, Delete) em um banco de dados relacional hospedado na nuvem (AWS RDS). O sistema atende aos requisitos da Parte 1 da disciplina de Engenharia de Dados.

## Funcionalidades

O programa interage com quatro tabelas principais do esquema:
* Usuario
* Estudante
* Curso
* Vinculo

Permite realizar insercoes, consultas, atualizacoes e exclusoes de dados diretamente pelo terminal, alem de gerar um relatorio consolidado utilizando juncoes (JOIN).

## Pre-requisitos

Antes de executar o projeto, certifique-se de ter instalado:
* Python 3.13 ou superior
* Driver de conexao do PostgreSQL para Python (psycopg2-binary)

## Instalacao

1. Instale a biblioteca necessaria para a conexao com o banco de dados:
```bash
python -m pip install psycopg2-binary
```
# Querys utilizadas no pgAdmin

## Tabela dimesão e Tabela de fatos

```bash
CREATE SCHEMA dw_universidade;

-- 1. Dimensao Professor
CREATE TABLE dw_universidade.dim_professor (
    sk_professor SERIAL PRIMARY KEY,
    mat_professor VARCHAR(7),        
    cpf NUMERIC(13),                 
    nome VARCHAR(100),               
    jornada_trabalho VARCHAR(3),    
    formacao VARCHAR(20),            
    departamento_lotacao VARCHAR(50) 
);

-- 2. Dimensao Disciplina
CREATE TABLE dw_universidade.dim_disciplina (
    sk_disciplina SERIAL PRIMARY KEY,
    codigo_disciplina VARCHAR(8),    
    nome VARCHAR(40),               
    cr_total SMALLINT                
);

-- 3. Dimensao Departamento
CREATE TABLE dw_universidade.dim_departamento (
    sk_departamento SERIAL PRIMARY KEY,
    codigo_dep VARCHAR(5),           
    nome VARCHAR(50)                
);

-- 4. Dimensao Semestre
CREATE TABLE dw_universidade.dim_semestre (
    sk_semestre SERIAL PRIMARY KEY,
    ano SMALLINT,                    
    periodo SMALLINT                 
);

-- 5. Dimensao Campus

CREATE TABLE dw_universidade.dim_campus (
    sk_campus SERIAL PRIMARY KEY,
    nome_campus VARCHAR(100)
);

-- 6. Tabela de Fatos
CREATE TABLE dw_universidade.fato_turma (
    sk_professor INT REFERENCES dw_universidade.dim_professor(sk_professor),
    sk_disciplina INT REFERENCES dw_universidade.dim_disciplina(sk_disciplina),
    sk_departamento INT REFERENCES dw_universidade.dim_departamento(sk_departamento),
    sk_semestre INT REFERENCES dw_universidade.dim_semestre(sk_semestre),
    sk_campus INT REFERENCES dw_universidade.dim_campus(sk_campus),
    
    qtd_discentes_matriculados INT,
    media_notes REAL,                
    qtd_aprovados INT,
    qtd_reprovados INT,
    
    PRIMARY KEY (sk_professor, sk_disciplina, sk_departamento, sk_semestre, sk_campus)
);

```

## Criação de usuário e suas permissões

```bash
CREATE USER usuario_hop WITH PASSWORD '********';

GRANT CONNECT ON DATABASE postgres TO usuario_hop;

GRANT USAGE, CREATE ON SCHEMA dw_universidade TO usuario_hop;

GRANT SELECT, INSERT, UPDATE, DELETE ON ALL TABLES IN SCHEMA dw_universidade TO usuario_hop;

GRANT USAGE, SELECT ON ALL SEQUENCES IN SCHEMA dw_universidade TO usuario_hop;

GRANT USAGE ON SCHEMA universidade TO usuario_hop;

GRANT SELECT ON ALL TABLES IN SCHEMA universidade TO usuario_hop;
```

# Populando o Banco

![]()



