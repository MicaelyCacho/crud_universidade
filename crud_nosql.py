import os
from pymongo import MongoClient
from bson import ObjectId

#CONFIGURAÇÃO DA CONEXÃO NO MONGODB
MONGO_URI = os.getenv("MONGO_URI", "mongodb+srv://lari_db_user:larilari1212@cluster0.altpe5p.mongodb.net/?appName=Cluster0")
client = MongoClient(MONGO_URI)
db = client["universidade_db"]

# Coleções
estudantes_col = db["estudantes"]
cursos_col = db["cursos"]

# ==========================================
#             CRUD: COLEÇÃO CURSOS
# ==========================================

def inserir_curso(nome, grau, turno, campus, nivel):
    try:
        curso = {
            "nome": nome,
            "grau": grau,
            "turno": turno,
            "campus": campus,
            "nivel": nivel
        }
        resultado = cursos_col.insert_one(curso)
        print(f"[Sucesso] Curso '{nome}' cadastrado com ID: {resultado.inserted_id}")
    except Exception as e:
        print(f"Erro ao inserir curso: {e}")

def listar_cursos():
    try:
        print("\n--- Lista de Cursos (NoSQL) ---")
        for curso in cursos_col.find():
            print(f"ID: {curso['_id']} | Nome: {curso['nome']} | Grau: {curso['grau']} | Turno: {curso['turno']}")
    except Exception as e:
        print(f"Erro ao listar cursos: {e}")

def atualizar_nome_curso(id_curso, novo_nome):
    try:
        resultado = cursos_col.update_one(
            {"_id": ObjectId(id_curso)},
            {"$set": {"nome": novo_nome}}
        )
        if resultado.modified_count > 0:
            print(f"[Sucesso] Nome do curso ID {id_curso} atualizado para '{novo_nome}'!")
        else:
            print("[Aviso] Curso não encontrado ou sem alterações.")
    except Exception as e:
        print(f"Erro ao atualizar curso: {e}")

def deletar_curso(id_curso):
    try:
        #Integridade Referencial via Aplicação: impede exclusão se houver vínculos ativos
        vinculo_ativo = estudantes_col.find_one({"vinculos.curso_id": ObjectId(id_curso)})
        if vinculo_ativo:
            print("[Erro IntegrityConstraint] Não é possível deletar o curso. Existem alunos vinculados a ele.")
            return

        resultado = cursos_col.delete_one({"_id": ObjectId(id_curso)})
        if resultado.deleted_count > 0:
            print(f"[Sucesso] Curso ID {id_curso} removido com sucesso!")
        else:
            print("[Aviso] Curso não encontrado.")
    except Exception as e:
        print(f"Erro ao deletar curso: {e}")


# ==========================================
#          CRUD: COLEÇÃO ESTUDANTES
# ==========================================

def inserir_usuario(cpf, nome, login, senha, emails):
    #Inicializa o documento na coleção estudantes apenas com dados cadastrais
    try:
        # Validação de Chave Única via aplicação para o CPF
        if estudantes_col.find_one({"cpf": cpf}):
            print("[Erro] Já existe um usuário cadastrado com este CPF.")
            return

        usuario = {
            "cpf": cpf,
            "nome": nome,
            "login": login,
            "senha": senha,
            "emails": emails,
            "matricula": None, # Ainda não é estudante
            "vinculos": []
        }
        estudantes_col.insert_one(usuario)
        print(f"[Sucesso] Usuário '{nome}' cadastrado com sucesso!")
    except Exception as e:
        print(f"Erro ao inserir usuário: {e}")

def listar_usuarios():
    try:
        print("\n--- Lista de Usuários no Banco (NoSQL) ---")
        for est in estudantes_col.find():
            print(f"CPF: {est['cpf']} | Nome: {est['nome']} | Login: {est['login']} | Emails: {est['emails']}")
    except Exception as e:
        print(f"Erro ao buscar dados: {e}")

def atualizar_senha_usuario(cpf, nova_senha):
    try:
        resultado = estudantes_col.update_one({"cpf": cpf}, {"$set": {"senha": nova_senha}})
        if resultado.modified_count > 0:
            print("[Sucesso] Senha atualizada com sucesso!")
        else:
            print("[Aviso] Usuário não encontrado ou senha idêntica.")
    except Exception as e:
        print(f"Erro ao atualizar senha: {e}")

def deletar_usuario(cpf):
    try:
        resultado = estudantes_col.delete_one({"cpf": cpf})
        if resultado.deleted_count > 0:
            print("[Sucesso] Usuário removido do sistema.")
        else:
            print("[Aviso] Usuário não encontrado.")
    except Exception as e:
        print(f"Erro ao deletar: {e}")


# ==========================================
#        TRANSPOSIÇÃO DA LOGICA DE ESTUDANTE
# ==========================================

def inserir_estudante(mat_estudante, cpf):
    #Efetua o 'Upgrade' do usuário para estudante, setando a matrícula
    try:
        # Validação de Chave Única para a matrícula
        if estudantes_col.find_one({"matricula": mat_estudante}):
            print("[Erro] Matrícula já existente no sistema.")
            return

        resultado = estudantes_col.update_one(
            {"cpf": cpf},
            {"$set": {"matricula": mat_estudante}}
        )
        if resultado.modified_count > 0:
            print(f"[Sucesso] Estudante de matrícula {mat_estudante} criado!")
        else:
            print("[Aviso] CPF não localizado para gerar matrícula.")
    except Exception as e:
        print(f"Erro ao inserir estudante: {e}")

def listar_estudantes():
    try:
        print("\n--- Lista de Estudantes ---")
        for est in estudantes_col.find({"matricula": {"$ne": None}}):
            print(f"Matrícula: {est['matricula']} | CPF do Usuário: {est['cpf']}")
    except Exception as e:
        print(f"Erro ao listar estudantes: {e}")

def atualizar_matricula_estudante(cpf, nova_matricula):
    try:
        resultado = estudantes_col.update_one({"cpf": cpf}, {"$set": {"matricula": nova_matricula}})
        if resultado.modified_count > 0:
            print(f"[Sucesso] Matrícula alterada com sucesso para '{nova_matricula}'!")
        else:
            print("[Aviso] Estudante não encontrado com esse CPF.")
    except Exception as e:
        print(f"Erro ao atualizar matrícula: {e}")

def deletar_estudante(mat_estudante):
    #Remove a flag de estudante voltando o registro para apenas usuário, limpando vínculos
    try:
        resultado = estudantes_col.update_one(
            {"matricula": mat_estudante},
            {"$set": {"matricula": None, "vinculos": []}}
        )
        if resultado.modified_count > 0:
            print(f"[Sucesso] Estudante de matrícula {mat_estudante} removido do escopo acadêmico!")
        else:
            print("[Aviso] Estudante não encontrado.")
    except Exception as e:
        print(f"Erro ao deletar estudante: {e}")


# ==========================================
#         TRANSPOSIÇÃO DA LOGICA DE VÍNCULO
# ==========================================

def inserir_vinculo(mat_estudante, id_curso, status):
    #Dá um push em um novo objeto dentro da lista interna de vínculos do estudante
    try:
        resultado = estudantes_col.update_one(
            {"matricula": mat_estudante},
            {"$push": {"vinculos": {"curso_id": ObjectId(id_curso), "status": status}}}
        )
        if resultado.modified_count > 0:
            print("[Sucesso] Vínculo entre estudante e curso criado com sucesso!")
        else:
            print("[Aviso] Matrícula não localizada para criar vínculo.")
    except Exception as e:
        print(f"Erro ao criar vínculo: {e}")

def atualizar_status_vinculo(mat_estudante, id_curso, novo_status):
    #Atualiza o status de um elemento específico da lista utilizando filtros posicionais
    try:
        resultado = estudantes_col.update_one(
            {"matricula": mat_estudante, "vinculos.curso_id": ObjectId(id_curso)},
            {"$set": {"vinculos.$.status": novo_status}}
        )
        if resultado.modified_count > 0:
            print(f"[Sucesso] Status do vínculo do aluno {mat_estudante} alterado para '{novo_status}'!")
        else:
            print("[Aviso] Vínculo não localizado para alteração.")
    except Exception as e:
        print(f"Erro ao atualizar vínculo: {e}")

def deletar_vinculo(mat_estudante, id_curso):
    #Efetua um pull para arrancar o subdocumento do array de vínculos
    try:
        resultado = estudantes_col.update_one(
            {"matricula": mat_estudante},
            {"$pull": {"vinculos": {"curso_id": ObjectId(id_curso)}}}
        )
        if resultado.modified_count > 0:
            print(f"[Sucesso] Vínculo do aluno {mat_estudante} foi removido!")
        else:
            print("[Aviso] Vínculo não encontrado.")
    except Exception as e:
        print(f"Erro ao deletar vínculo: {e}")


# ==========================================
#          REPOSITÓRIO / RELATÓRIO GLOBAL
# ==========================================

def listar_estudantes_completos():
    #Simula o JOIN original combinando coleções via Pipeline de Aggregation ($lookup)
    try:
        pipeline = [
            {"$match": {"matricula": {"$ne": None}}},
            {"$unwind": "$vinculos"},
            {
                "$lookup": {
                    "from": "cursos",
                    "localField": "vinculos.curso_id",
                    "foreignField": "_id",
                    "as": "curso_detalhe"
                }
            },
            {"$unwind": "$curso_detalhe"},
            {
                "$project": {
                    "nome": 1,
                    "matricula": 1,
                    "nome_curso": "$curso_detalhe.nome",
                    "status": "$vinculos.status"
                }
            }
        ]
        
        registros = estudantes_col.aggregate(pipeline)
        print("\n--- Relatório Geral de Estudantes Vinculados (NoSQL) ---")
        for linha in registros:
            print(f"Nome: {linha['nome']} | Matrícula: {linha['matricula']} | Curso: {linha['nome_curso']} | Status: {linha['status']}")
    except Exception as e:
        print(f"Erro no relatório: {e}")