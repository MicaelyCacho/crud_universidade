# ===================================
# SELETOR DE MOTOR DE BANCO DE DADOS
# ===================================
import sys
print("="*50)
print("   SELECIONE O MOTOR DE BANCO DE DADOS PARA O TESTE")
print("="*50)
print(" [1] PostgreSQL (Parte 1 - Relacional AWS RDS)")
print(" [2] MongoDB    (Parte 2 - NoSQL AWS / Atlas)")
print("="*50)
motor_escolhido = input("Escolha o motor (1 ou 2): ")

if motor_escolhido == "2":
    print("\n[INFO] Redirecionando operações para o MongoDB...")
    from init_db import inicializar_banco_nosql
    inicializar_banco_nosql() #Garante a criação dos Schemas e Índices
    
    # Importa as funções NoSQL com os mesmos nomes das relacionais,
    # fazendo com que o menu abaixo chame o MongoDB sem alterar o código
    from crud_nosql import (
        inserir_usuario, listar_usuarios, atualizar_senha_usuario, deletar_usuario,
        inserir_curso, listar_cursos, atualizar_nome_curso, deletar_curso,
        inserir_estudante, listar_estudantes, atualizar_matricula_estudante, deletar_estudante,
        inserir_vinculo, atualizar_status_vinculo, deletar_vinculo, listar_estudantes_completos
    )
elif motor_escolhido != "1":
    print("[Erro] Opção inválida. Encerrando o sistema.")
    sys.exit()
else:
    print("\n[INFO] Executando motor padrão PostgreSQL...")

from crud_universidade import (
    inserir_usuario, listar_usuarios, atualizar_senha_usuario, deletar_usuario,
    inserir_curso, listar_cursos, atualizar_nome_curso, deletar_curso,
    inserir_estudante, listar_estudantes, atualizar_matricula_estudante, deletar_estudante,
    inserir_vinculo, atualizar_status_vinculo, deletar_vinculo, listar_estudantes_completos
)

def exibir_menu():
    while True:
        print("\n" + "="*50)
        print("     SISTEMA ACADÊMICO - CRUD UNIVERSIDADE"  )
        print("="*50)
        print(" [1]  Cadastrar Usuario")
        print(" [2]  Listar Usuarios")
        print(" [3]  Atualizar Senha de Usuario")
        print(" [4]  Deletar Usuario")
        print("-"*50)
        print(" [5]  Cadastrar Novo Curso")
        print(" [6]  Listar Cursos")
        print(" [7]  Atualizar Nome de um Curso")
        print(" [8]  Deletar um Curso")
        print("-"*50)
        print(" [9]  Matricular Usuario como Estudante")
        print(" [10] Listar Apenas Estudantes (Matricula/CPF)")
        print(" [11] Alterar Matricula de um Estudante")
        print(" [12] Remover Registro de Estudante")
        print("-"*50)
        print(" [13] Vincular Estudante a um Curso")
        print(" [16] Listar estudantes com todos os detalhes (Relatório Global)")
        print(" [14] Alterar Status de Vínculo de Aluno")
        print(" [15] Remover Vínculo de Aluno")
        print("-"*50)
        print(" [0]  Sair")
        print("="*50)
        
        opcao = input("Escolha uma opcao: ")
        
        # --- OPERAÇÕES: USUÁRIO ---
        if opcao == "1":
            print("\n--- Cadastrar Usuario ---")
            cpf = int(input("CPF (Apenas numeros): "))
            nome = input("Nome Completo: ")
            login = input("Login de acesso: ")
            senha = input("Senha: ")
            email = input("E-mail: ")
            inserir_usuario(cpf, nome, login, senha, [email])
            
        elif opcao == "2":
            listar_usuarios()
            
        elif opcao == "3":
            print("\n--- Atualizar Senha ---")
            cpf = int(input("CPF do usuario: "))
            nova_senha = input("Nova senha: ")
            atualizar_senha_usuario(cpf, nova_senha)
            
        elif opcao == "4":
            print("\n--- Deletar Usuario ---")
            cpf = int(input("CPF do usuario a deletar: "))
            deletar_usuario(cpf)
            
        # --- OPERAÇÕES: CURSO ---
        elif opcao == "5":
            print("\n--- Cadastrar Curso ---")
            nome = input("Nome do Curso: ")
            grau = input("Grau (Bacharelado/Licenciatura/Tecnologo): ")
            turno = input("Turno (Matutino/Vespertino/Noturno/Integral): ")
            campus = input("Campus: ")
            nivel = input("Nivel (Graduacao/Pos-Graduacao): ")
            inserir_curso(nome, grau, turno, campus, nivel)
            
        elif opcao == "6":
            listar_cursos()
            
        elif opcao == "7":
            print("\n--- Atualizar Curso ---")
            id_c = int(input("ID do Curso que deseja alterar: "))
            novo_n = input("Novo nome do Curso: ")
            atualizar_nome_curso(id_c, novo_n)
            
        elif opcao == "8":
            print("\n--- Deletar Curso ---")
            id_c = int(input("ID do Curso que deseja deletar: "))
            deletar_curso(id_c)
            
        # --- OPERAÇÕES: ESTUDANTE ---
        elif opcao == "9":
            print("\n--- Matricular Estudante ---")
            mat = input("Digite uma nova matricula: ")
            cpf = int(input("Digite o CPF do usuario ja cadastrado: "))
            inserir_estudante(mat, cpf)
            
        elif opcao == "10":
            listar_estudantes()
            
        elif opcao == "11":
            print("\n--- Alterar Matricula ---")
            cpf = int(input("Digite o CPF do estudante: "))
            nova_mat = input("Digite a nova Matricula: ")
            atualizar_matricula_estudante(cpf, nova_mat)
            
        elif opcao == "12":
            print("\n--- Remover Estudante ---")
            mat = input("Digite a matricula do estudante a remover: ")
            deletar_estudante(mat)
            
        # --- OPERAÇÕES: VÍNCULO ---
        elif opcao == "13":
            print("\n--- Vincular Estudante a Curso ---")
            mat = input("Matricula do Estudante: ")
            id_curso = int(input("ID do Curso: "))
            status = input("Status inicial (Ativo/Trancado/Formando/Graduado): ")
            inserir_vinculo(mat, id_curso, status)
            
        elif opcao == "14":
            print("\n--- Alterar Status de Vinculo ---")
            mat = input("Matricula do Estudante: ")
            id_c = int(input("ID do Curso: "))
            novo_st = input("Novo Status (Ativo/Trancado/Formando/Graduado): ")
            atualizar_status_vinculo(mat, id_c, novo_st)
            
        elif opcao == "15":
            print("\n--- Remover Vinculo ---")
            mat = input("Matricula do Estudante: ")
            id_c = int(input("ID do Curso: "))
            deletar_vinculo(mat, id_c)
            
        # --- RELATÓRIO GLOBAL ---
        elif opcao == "16":
            listar_estudantes_completos()
            
        elif opcao == "0":
            print("\nEncerrando o sistema academico...")
            break
        else:
            print("\n[Erro] Opção invalida! Escolha um numero do menu.")

if __name__ == "__main__":
    exibir_menu()