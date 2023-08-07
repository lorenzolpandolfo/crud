import database
import create


def menu(database):
    try:
        escolha = int(input("(1) Criar" + ' '*10 + '│ (5) Configurações\n' + "(2) Ler" + ' '*12 + '│' + ' (6) Sair' + "\n(3) Atualizar      │" + "\n(4) Deletar        │\n> Selecione a opção: "))

        if escolha == 1:
            create.create(database)
            return menu(database)
        
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
    escolha = int(input('\n----- Configurações -----\n(1) Alterar database\n> Selecione a opção: '))
    try:
        if escolha == 1:
            print('\n[-] Registre a sua nova database:')
            return menu(database.registrar_database())
                
        else:
            return menu(database)
        
    except Exception:
        print('[x] Valor inválido.\n')
        return menu(database)


if __name__ == '__main__':
    database = database.Banco.checar_database_registrada()
    menu(database)
