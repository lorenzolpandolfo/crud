import mysql.connector
import json

class Banco:
    def __init__(self, conexao, cursor):
        self.conexao = conexao
        self.cursor = cursor

    # interage com os atributos: altera o self.conexao e self.cursor
    @classmethod
    def conectar(cls):
        try:
            with open('data.json', 'r', encoding='utf8') as arquivo:
                dados = json.load(arquivo)
                login = dados['database']

                conexao = mysql.connector.connect(
                    host=login['host'],
                    user=login['user'],
                    password=login['password'],
                    database=login['database']
                )
                cursor = conexao.cursor()
                database = cls(conexao, cursor)
                print(f'[!] Conectado em {login["database"]} como {login["user"]}.')
                return database
        
        except (FileNotFoundError, KeyError, mysql.connector.Error) as erro:
            print(f"[x] Houve um erro ao conectar-se com o banco de dados:\n └─ {erro}. \n\n> Registre novamente a sua database:")
            return cls.registrar_database()
    
    @staticmethod
    def registrar_database():
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
        return Banco.conectar()
    
    @staticmethod
    def checar_database_registrada():
        """
        Abre o arquivo que contém a database salva e confere se as informações
        estão salvas corretamente. Se estiverem, tenta conectar, senão, retorna
        a função de registrar uma nova database.
        """
        try:
            with open('data.json', 'r', encoding='utf8') as arquivo:
                dados = json.load(arquivo)
                login = dados['database']
                esperado = ['host', 'user', 'password', 'database']

                for e in esperado:
                    if e not in login or not login[e]:
                        print(f'[x] Não há {e} registrado na database.\n[-] Registre a sua database:')
                        return Banco.registrar_database()

                return Banco.conectar()

        except (FileNotFoundError, KeyError, json.JSONDecodeError):
            print("[x] Não foi encontrada nenhuma database registrada no arquivo.\n[-] Registre a sua database:")
            return Banco.registrar_database()
