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
