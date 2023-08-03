import mysql.connector

conexao = mysql.connector.connect(
    host = 'localhost',
    user = 'root',
    password = 'lorenzo',
    database = 'database'
)

# executa os comandos
cursor = conexao.cursor()


produto = 'Minecraft'
valor = 4

# o comando deve estar com aspas simples
# dentro do parenteses tem a ordem de inserção de informações
# o id_vendas é autoincrement, ele se auto-preenche
# o "" no produto é necessário pq no mysql precisa de aspas em str
#comando = f'INSERT INTO vendas (nome_produto, valor_produto) VALUES ("{produto}", {valor})'
comando = f'SELECT * FROM vendas'
cursor.execute(comando)

# executa o commit
#conexao.commit()


def create(tabela, ):




# ler o banco de dados
resultado = cursor.fetchall()
print(resultado)


cursor.close()
conexao.close()
