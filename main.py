import mysql.connector
import json
from prettytable import PrettyTable

class Banco:
    def __init__(self, conexao, cursor):
        self.conexao = conexao
        self.cursor = cursor


def conectar(h, u, p, d):
    try:
        conexao = mysql.connector.connect(
            host = h,
            user = u,
            password = p,
            database = d
        )
        cursor = conexao.cursor()
        database = Banco(conexao, cursor)
        
        print(f'[!] Conectado em {d} como {u}.')
        return menu(database)

    except mysql.connector.Error as erro:
        print(f"[x] Houve um erro ao conectar-se com o banco de dados:\n └─ {erro}. \n\n> Registre novamente a sua database:")
        return registar_database()


def registar_database():
    host = input('> Host: ')
    user = input('> User: ')
    password = input('> Senha: ')
    database = input('> Database: ')

    login = {
    "database": {
        "host": host,
        "user": user,
        "password": password,
        "database": database
        }
    }

    with open('data.json', 'w', encoding='utf8') as arquivo:
        arquivo.write(json.dumps(login))
        arquivo.close()

    print('[+] Database registrada. O login será automático na próxima sessão.\n[-] Realizando login...\n')
    return conectar(host, user, password, database)


def checar_database_registrada():
        try:
            with open('data.json', 'r', encoding='utf8') as arquivo:
                dados = json.load(arquivo)
                login = dados['database']

                esperado = ['host', 'user', 'password', 'database']
                
                for i, e in enumerate(esperado):
                    if e in login:
                        if login[e] == 0:
                            # Está faltando alguma informação no login
                            print(f'[x] Não há {e} registrado na database.\n[-] Registre a sua database:')
                            return registar_database()
                            
                        else:
                            # todos os elementos estao presentes
                            if i == 3:
                                return conectar(
                                    login['host'],
                                    login['user'],
                                    login['password'],
                                    login['database']
                                )
                                
                    else:
                        print('[x] Não há {e} no arquivo.\n[-] Registre a sua database:')
                        return registar_database()
        
        except Exception as err:
            print(f"{err} [x] Não foi encontrada nenhuma database registrada no arquivo.\n[-] Registre a sua database:")
            return registar_database()


def menu(database):
    try:
        escolha = int(input("(1) Criar" + ' '*10 + '│ (5) Configurações\n' + "(2) Ler" + ' '*12 + '│' + ' (6) Sair' + "\n(3) Atualizar      │" + "\n(4) Deletar        │\n> Selecione a opção: "))

        if escolha == 1:
            return create(database)
        
        elif escolha == 2:
            pass

        elif escolha == 3:
            pass

        elif escolha == 4:
            pass
        
        elif escolha == 5:
            return config(database)
        
        elif escolha == 6:
            return 0

    except Exception:
        print("[x] Valor inválido.\n")
        return menu(database)


def config(database):
    escolha = int(input('\n[-] Configurações\n(1) Alterar database\n> Selecione a opção: '))
    try:
        if escolha == 1:
            print('\n[-] Registre a sua nova database:')
            return registar_database()
        else:
            return menu(database)
        
    except Exception:
        print('[x] Valor inválido.\n')
        return menu(database)


def create(database):
    conexao = database.conexao
    cursor = database.cursor
    ptable = PrettyTable()
    
    print('\n----- Criar -----')
    tabela = input('> Tabela: ')

    # adquirindo a quantidade de colunas na tabela
    cursor.execute(f"SHOW COLUMNS FROM {tabela}")
    colunas = cursor.fetchall()
    f_colunas = ' │ '.join(str(coluna[0]) for coluna in colunas)
    tt = len(f_colunas) - len(tabela)
    view_tabela = "\n" + "-"*int(tt/2) + f" {tabela} "+ "-"*(int(tt/2)-1) + f"\n{f_colunas}\n" + "-"*len(f_colunas)
    print(view_tabela)
    f_col = []
    novos_valores = []

    for coluna in colunas:
        nome_coluna = coluna[0]
        
        if coluna[5] == 'auto_increment':
            print(f'[-] A coluna {nome_coluna} é preenchida automaticamente.')
        
        else:
            f_col.append(nome_coluna)
            value = input(f'> Digite o valor para a coluna {nome_coluna}: ')
            novos_valores.append(value)

    f_resultado = ' │ '.join(str(e) for e in novos_valores)

    # criando a pretty table
    ptable.field_names = f_col
    ptable.add_row(novos_valores)
    
    escolha = input(f"\n[-] O resultado será:\n{ptable}\n[?] Você deseja confirmar a operação? (S/n): ")
    if escolha.upper == 'S' or escolha == '':
        try:
            teste = ', '.join(str(e) if colunas[i][5] != 'auto_increment' else f'"{e}"' for i, e in enumerate(novos_valores))
            colunas_alteradas = ', '.join(str(c[0]) for c in colunas if c[5] != 'auto_increment')
            cursor.execute(f'INSERT INTO {tabela} ({colunas_alteradas}) VALUES ({teste})')
            conexao.commit()
            print('[!] Coluna criada com sucesso.\n')
            return menu(database)
        
        except Exception as erro:
            print(f'[x] Houve um erro ao alterar o banco de dados:\n └─ {erro}.\n')
            return menu(database)

    else:
        print('[x] Operação cancelada pelo usuário.\n')
        return menu(database)


if __name__ == '__main__':
    checar_database_registrada()
    #conexao = conectar()

# executa os comandos
#cursor = conexao.cursor()

#produto = 'Minecraft'
#valor = 4

# o comando deve estar com aspas simples
# dentro do parenteses tem a ordem de inserção de informações
# o id_vendas é autoincrement, ele se auto-preenche
# o "" no produto é necessário pq no mysql precisa de aspas em str
#comando = f'INSERT INTO vendas (nome_produto, valor_produto) VALUES ("{produto}", {valor})'
#comando = f'SELECT * FROM vendas'
#cursor.execute(comando)

# executa o commit
#conexao.commit()

# ler o banco de dados
# resultado = cursor.fetchall()
# print(resultado)

#cursor.close()
#conexao.close()
