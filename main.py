import mysql.connector
import json

class Usuario:
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
        user = Usuario(conexao, cursor)
        
        print(f'[!] Conectado em {d} como {u}.')
        menu(user)

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

    print('[+] Database registrada. O login será automático na próxima sessão.\n[-] Realizando login...\n')
    conectar(host, user, password, database)


def checar_database_registrada():
    with open('data.json', 'r', encoding='utf8') as arquivo:
        try:
            dados = json.load(arquivo)
            login = dados['database']

            esperado = ['host', 'user', 'password', 'database']
            
            for i, e in enumerate(esperado):
                if e in login:
                    if login[e] == 0:
                        # Está faltando alguma informação no login
                        print(f'[x] Não há {e} registrado na database.\n[-] Registre a sua database:')
                        registar_database()
                        break
                    else:
                        # todos os elementos estao presentes
                        if i == 3:
                            conectar(
                                login['host'],
                                login['user'],
                                login['password'],
                                login['database']
                            )
                else:
                    print('[x] Não há {e} no arquivo.')
        
        except Exception:
            print("[X] Não foi encontrada nenhuma database registrada no arquivo.")
            registar_database()


def menu(user):
    print(user.conexao)
    escolha = int(input("(1) Criar\n(2) Ler\n(3) Atualizar\n(4) Deletar\n> Selecione a opção: "))
    try:
        if escolha == 1:
            pass
        
        elif escolha == 2:
            pass

        elif escolha == 3:
            pass

        elif escolha == 4:
            pass
        
        else:
            return 0
    
    except Exception:
        print("[x] Valor inválido.\n")
        menu()


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


def create(tabela, ):
    pass



# ler o banco de dados
# resultado = cursor.fetchall()
# print(resultado)


#cursor.close()
#conexao.close()
