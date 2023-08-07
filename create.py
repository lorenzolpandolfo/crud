from prettytable import PrettyTable

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
            return True
        
        except Exception as erro:
            print(f'[x] Houve um erro ao alterar o banco de dados:\n └─ {erro}.\n')
            return False

    else:
        print('[x] Operação cancelada pelo usuário.\n')
        return False