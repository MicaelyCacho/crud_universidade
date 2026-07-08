#pip install psycopg2-binary
import psycopg2
from psycopg2 import Error

# === CONFIGURAÇÃO DA CONEXÃO ===
DB_HOST = "database-1.c0d8hrkmngei.us-east-1.rds.amazonaws.com"
DB_NAME = "postgres"
DB_USER = "postgres"
DB_PASS = "12345678"
DB_PORT = "5432"

def obter_conexao():
    try:
        conexao = psycopg2.connect(
            host=DB_HOST,
            database=DB_NAME,
            user=DB_USER,
            password=DB_PASS,
            port=DB_PORT
        )
        return conexao
    except Error as e:
        print(f"Erro ao conectar ao banco na AWS: {e}")
        return None

# ==========================================
#             CRUD: TABELA USUARIO
# ==========================================

# === CREATE ===
def inserir_usuario(cpf, nome, login, senha, emails, data_nascimento=None):
    sql = """
    INSERT INTO universidade.usuario (cpf, nome, login, senha, email, data_nascimento)
    VALUES (%s, %s, %s, %s, %s, %s);
    """
    conn = obter_conexao()
    if conn:
        try:
            cursor = conn.cursor()
            cursor.execute(sql, (cpf, nome, login, senha, emails, data_nascimento))
            conn.commit()
            print(f"[Sucesso] Usuário '{nome}' cadastrado com sucesso!")
        except Error as e:
            print(f"Erro ao inserir usuário: {e}")
            conn.rollback()
        finally:
            cursor.close()
            conn.close()

# === READ ===
def listar_usuarios():
    sql = "SELECT cpf, nome, login, email FROM universidade.usuario;"
    conn = obter_conexao()
    if conn:
        try:
            cursor = conn.cursor()
            cursor.execute(sql)
            registros = cursor.fetchall()
            
            print("\n--- Lista de Usuários no Banco ---")
            for linha in registros:
                print(f"CPF: {linha[0]} | Nome: {linha[1]} | Login: {linha[2]} | Emails: {linha[3]}")
        except Error as e:
            print(f"Erro ao buscar dados: {e}")
        finally:
            cursor.close()
            conn.close()

# === UPDATE ===
def atualizar_senha_usuario(cpf, nova_senha):
    sql = "UPDATE universidade.usuario SET senha = %s WHERE cpf = %s;"
    conn = obter_conexao()
    if conn:
        try:
            cursor = conn.cursor()
            cursor.execute(sql, (nova_senha, cpf))
            conn.commit()
            if cursor.rowcount > 0:
                print("[Sucesso] Senha atualizada com sucesso!")
            else:
                print("[Aviso] Usuário não encontrado com esse CPF.")
        except Error as e:
            print(f"Erro ao atualizar senha: {e}")
            conn.rollback()
        finally:
            cursor.close()
            conn.close()

# === DELETE ===
def deletar_usuario(cpf):
    sql = "DELETE FROM universidade.usuario WHERE cpf = %s;"
    conn = obter_conexao()
    if conn:
        try:
            cursor = conn.cursor()
            cursor.execute(sql, (cpf,))
            conn.commit()
            print("[Sucesso] Usuário removido do sistema.")
        except Error as e:
            print(f"Erro ao deletar: {e}")
            conn.rollback()
        finally:
            cursor.close()
            conn.close()


# ==========================================
#             CRUD: TABELA CURSO
# ==========================================

def inserir_curso(nome, grau, turno, campus, nivel):
    sql = """
    INSERT INTO universidade.curso (nome, grau, turno, campus, nivel)
    VALUES (%s, %s, %s, %s, %s);
    """
    conn = obter_conexao()
    if conn:
        try:
            cursor = conn.cursor()
            cursor.execute(sql, (nome, grau, turno, campus, nivel))
            conn.commit()
            print(f"[Sucesso] Curso '{nome}' cadastrado!")
        except Error as e:
            print(f"Erro ao inserir curso: {e}")
            conn.rollback()
        finally:
            cursor.close()
            conn.close()

def listar_cursos():
    sql = "SELECT idCurso, nome, grau, turno FROM universidade.curso;"
    conn = obter_conexao()
    if conn:
        try:
            cursor = conn.cursor()
            cursor.execute(sql)
            for linha in cursor.fetchall():
                print(f"ID: {linha[0]} | Nome: {linha[1]} | Grau: {linha[2]} | Turno: {linha[3]}")
        except Error as e:
            print(f"Erro ao listar cursos: {e}")
        finally:
            cursor.close()
            conn.close()

def atualizar_nome_curso(id_curso, novo_nome):
    sql = "UPDATE universidade.curso SET nome = %s WHERE idCurso = %s;"
    conn = obter_conexao()
    if conn:
        try:
            cursor = conn.cursor()
            cursor.execute(sql, (novo_nome, id_curso))
            conn.commit()
            if cursor.rowcount > 0:
                print(f"[Sucesso] Nome do curso ID {id_curso} atualizado para '{novo_nome}'!")
            else:
                print("[Aviso] Curso não encontrado.")
        except Error as e:
            print(f"Erro ao atualizar curso: {e}")
            conn.rollback()
        finally:
            cursor.close()
            conn.close()

def deletar_curso(id_curso):
    sql = "DELETE FROM universidade.curso WHERE idCurso = %s;"
    conn = obter_conexao()
    if conn:
        try:
            cursor = conn.cursor()
            cursor.execute(sql, (id_curso,))
            conn.commit()
            if cursor.rowcount > 0:
                print(f"[Sucesso] Curso ID {id_curso} removido com sucesso!")
            else:
                print("[Aviso] Curso não encontrado.")
        except Error as e:
            print(f"Erro ao deletar curso: {e}. Verifique se existem alunos vinculados a ele.")
            conn.rollback()
        finally:
            cursor.close()
            conn.close()

# ==========================================
#             CRUD: TABELA ESTUDANTE
# ==========================================

def inserir_estudante(mat_estudante, cpf):
    sql = "INSERT INTO universidade.estudante (mat_estudante, cpf) VALUES (%s, %s);"
    conn = obter_conexao()
    if conn:
        try:
            cursor = conn.cursor()
            cursor.execute(sql, (mat_estudante, cpf))
            conn.commit()
            print(f"[Sucesso] Estudante de matrícula {mat_estudante} criado!")
        except Error as e:
            print(f"Erro ao inserir estudante: {e}")
            conn.rollback()
        finally:
            cursor.close()
            conn.close()

def listar_estudantes():
    """READ: Lista todos os estudantes cadastrados (Matrícula e CPF)"""
    sql = "SELECT mat_estudante, cpf FROM universidade.estudante;"
    conn = obter_conexao()
    if conn:
        try:
            cursor = conn.cursor()
            cursor.execute(sql)
            print("\n--- Lista de Estudantes ---")
            for linha in cursor.fetchall():
                print(f"Matrícula: {linha[0]} | CPF do Usuário: {linha[1]}")
        except Error as e:
            print(f"Erro ao listar estudantes: {e}")
        finally:
            cursor.close()
            conn.close()

def atualizar_matricula_estudante(cpf, nova_matricula):
    """UPDATE: Altera a matrícula de um estudante baseado no seu CPF"""
    sql = "UPDATE universidade.estudante SET mat_estudante = %s WHERE cpf = %s;"
    conn = obter_conexao()
    if conn:
        try:
            cursor = conn.cursor()
            cursor.execute(sql, (nova_matricula, cpf))
            conn.commit()
            if cursor.rowcount > 0:
                print(f"[Sucesso] Matrícula alterada com sucesso para '{nova_matricula}'!")
            else:
                print("[Aviso] Estudante não encontrado com esse CPF.")
        except Error as e:
            print(f"Erro ao atualizar matrícula: {e}")
            conn.rollback()
        finally:
            cursor.close()
            conn.close()

def deletar_estudante(mat_estudante):
    """DELETE: Remove o registro do estudante usando a matrícula"""
    sql = "DELETE FROM universidade.estudante WHERE mat_estudante = %s;"
    conn = obter_conexao()
    if conn:
        try:
            cursor = conn.cursor()
            cursor.execute(sql, (mat_estudante,))
            conn.commit()
            if cursor.rowcount > 0:
                print(f"[Sucesso] Estudante de matrícula {mat_estudante} removido!")
            else:
                print("[Aviso] Estudante não encontrado.")
        except Error as e:
            print(f"Erro ao deletar estudante: {e}. Verifique se ele possui vínculos ativos.")
            conn.rollback()
        finally:
            cursor.close()
            conn.close()            

# ==========================================
#             CRUD: TABELA VÍNCULO
# ==========================================

def inserir_vinculo(mat_estudante, id_curso, status):
    sql = "INSERT INTO universidade.vinculo (mat_estudante, curso, status) VALUES (%s, %s, %s);"
    conn = obter_conexao()
    if conn:
        try:
            cursor = conn.cursor()
            cursor.execute(sql, (mat_estudante, id_curso, status))
            conn.commit()
            print("[Sucesso] Vínculo entre estudante e curso criado com sucesso!")
        except Error as e:
            print(f"Erro ao criar vínculo: {e}")
            conn.rollback()
        finally:
            cursor.close()
            conn.close()

# === READ (Relatório de Alunos) ===
def listar_estudantes_completos():
    sql = """
    SELECT u.nome, e.mat_estudante, c.nome, v.status
    FROM universidade.usuario u
    JOIN universidade.estudante e ON u.cpf = e.cpf
    JOIN universidade.vinculo v ON e.mat_estudante = v.mat_estudante
    JOIN universidade.curso c ON v.curso = c.idCurso;
    """
    conn = obter_conexao()
    if conn:
        try:
            cursor = conn.cursor()
            cursor.execute(sql)
            print("\n--- Relatório Geral de Estudantes Vinculados ---")
            for linha in cursor.fetchall():
                print(f"Nome: {linha[0]} | Matrícula: {linha[1]} | Curso: {linha[2]} | Status: {linha[3]}")
        except Error as e:
            print(f"Erro no relatório: {e}")
        finally:
            cursor.close()
            conn.close()


def atualizar_status_vinculo(mat_estudante, id_curso, novo_status):
    sql = "UPDATE universidade.vinculo SET status = %s WHERE mat_estudante = %s AND curso = %s;"
    conn = obter_conexao()
    if conn:
        try:
            cursor = conn.cursor()
            cursor.execute(sql, (novo_status, mat_estudante, id_curso))
            conn.commit()
            if cursor.rowcount > 0:
                print(f"[Sucesso] Status do vínculo do aluno {mat_estudante} alterado para '{novo_status}'!")
            else:
                print("[Aviso] Vínculo não encontrado para esta combinação de Aluno e Curso.")
        except Error as e:
            print(f"Erro ao atualizar vínculo: {e}")
            conn.rollback()
        finally:
            cursor.close()
            conn.close()

def deletar_vinculo(mat_estudante, id_curso):
    sql = "DELETE FROM universidade.vinculo WHERE mat_estudante = %s AND curso = %s;"
    conn = obter_conexao()
    if conn:
        try:
            cursor = conn.cursor()
            cursor.execute(sql, (mat_estudante, id_curso))
            conn.commit()
            if cursor.rowcount > 0:
                print(f"[Sucesso] Vínculo do aluno {mat_estudante} foi removido!")
            else:
                print("[Aviso] Vínculo não encontrado.")
        except Error as e:
            print(f"Erro ao deletar vínculo: {e}")
            conn.rollback()
        finally:
            cursor.close()
            conn.close()