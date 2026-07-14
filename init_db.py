import os
from pymongo import MongoClient
from pymongo.errors import CollectionInvalid, OperationFailure

#CONFIGURAÇÃO DA CONEXÃO
MONGO_URI = os.getenv("MONGO_URI", "mongodb+srv://<usuario>:<senha>@cluster0.altpe5p.mongodb.net/?appName=Cluster0")
DB_NAME = "universidade_db"

def inicializar_banco_nosql():
    print("Iniciando conexão com o MongoDB na AWS...")
    client = MongoClient(MONGO_URI)
    db = client[DB_NAME]
    
    # ==========================================
    # 1. ESQUEMA DE VALIDAÇÃO: COLEÇÃO 'CURSOS'
    # ==========================================
    esquema_cursos = {
        "$jsonSchema": {
            "bsonType": "object",
            "required": ["nome", "grau", "turno", "campus", "nivel"],
            "properties": {
                "nome": {
                    "bsonType": "string",
                    "description": "'nome' deve ser uma string e é obrigatório."
                },
                "grau": {
                    "enum": ["Bacharelado", "Licenciatura", "Tecnólogo"],
                    "description": "'grau' deve pertencer estritamente ao domínio definido."
                },
                "turno": {
                    "enum": ["Matutino", "Vespertino", "Noturno", "Integral"],
                    "description": "'turno' deve pertencer estritamente ao domínio definido."
                },
                "campus": {
                    "bsonType": "string",
                    "description": "'campus' deve ser uma string e é obrigatório."
                },
                "nivel": {
                    "enum": ["Graduação", "Pós-Graduação"],
                    "description": "'nivel' deve ser Graduação ou Pós-Graduação."
                }
            }
        }
    }

    # ==========================================
    # 2. ESQUEMA DE VALIDAÇÃO: COLEÇÃO 'ESTUDANTES'
    # ==========================================
    esquema_estudantes = {
        "$jsonSchema": {
            "bsonType": "object",
            "required": ["cpf", "nome", "login", "senha", "emails"],
            "properties": {
                "cpf": {
                    "bsonType": "long",
                    "description": "'cpf' deve ser um inteiro longo (Int64) e é obrigatório."
                },
                "nome": {
                    "bsonType": "string",
                    "description": "'nome' deve ser uma string."
                },
                "login": {
                    "bsonType": "string",
                    "description": "'login' deve ser uma string."
                },
                "senha": {
                    "bsonType": "string",
                    "description": "'senha' de acesso é obrigatória."
                },
                "emails": {
                    "bsonType": "array",
                    "items": {"bsonType": "string"},
                    "description": "'emails' deve ser uma lista de strings contendo ao menos um e-mail."
                },
                "matricula": {
                    "bsonType": ["string", "null"],
                    "description": "'matricula' pode ser nula (usuário comum) ou string (estudante)."
                },
                "vinculos": {
                    "bsonType": "array",
                    "description": "Lista de cursos que o estudante possui vínculo.",
                    "items": {
                        "bsonType": "object",
                        "required": ["curso_id", "status"],
                        "properties": {
                            "curso_id": {
                                "bsonType": "objectId",
                                "description": "Deve referenciar um ID existente da coleção cursos."
                            },
                            "status": {
                                "enum": ["Ativo", "Trancado", "Formando", "Graduado"],
                                "description": "Restrição de domínio para o status do vínculo acadêmico."
                            }
                        }
                    }
                }
            }
        }
    }

    # ==========================================
    # 3. CRIAÇÃO DAS COLECÕES COM OS SCHEMAS
    # ==========================================
    colecoes = {
        "cursos": esquema_cursos,
        "estudantes": esquema_estudantes
    }

    for nome_col, esquema in colecoes.items():
        try:
            db.create_collection(nome_col, validator=esquema)
            print(f"Coleção '{nome_col}' criada com sucesso com regras de validação!")
        except CollectionInvalid:
            # Se a coleção já existe, atualizamos o validador dela
            print(f"Coleção '{nome_col}' já existente. Atualizando regras de validação de esquema...")
            db.command("collMod", nome_col, validator=esquema)
            print(f"Validador da coleção '{nome_col}' atualizado com sucesso!")
        except OperationFailure as err:
            print(f"Erro operacional na coleção '{nome_col}': {err}")

    # ==========================================
    # 4. CRIAÇÃO DE ÍNDICES ÚNICOS (RESTRIÇÃO DE CHAVE)
    # ==========================================
    print("\nConfigurando restrições de chaves únicas (Índices)...")
    try:
        # CPF único em toda a coleção
        res_cpf = db["estudantes"].create_index("cpf", unique=True)
        print(f"Índice de chave única gerado: {res_cpf}")
        
        # Matrícula única, ignorando documentos onde o valor é nulo (usuários normais)
        res_mat = db["estudantes"].create_index(
            "matricula", 
            unique=True, 
            partialFilterExpression={"matricula": {"$type": "string"}}
        )
        print(f"Índice de chave única (parcial) gerado para Estudantes: {res_mat}")
        print("\nInfraestrutura de Banco NoSQL pronta para operações CRUD!")
        
    except Exception as e:
        print(f"Falha ao tentar criar os índices no banco: {e}")

if __name__ == "__main__":
    inicializar_banco_nosql()