'''
docker: https://github.com/dajobe/hbase-docker
'''
from views import initialLoginView
import happybase
import re

is_num = re.compile('\d+')


def instruction_menu():
    # define sections
    queries = [
        {'label': 'vista de inicio de sesion', 'func': initialLoginView},
    ]
    # show menu
    count = 1
    for i in queries:
        print(f'{count}: - {i["label"]}')
        count += 1
    print(f'{count}: - salir')
    selection = input('su seleccion es: ')
    # get proper handler
    if is_num.match(selection):
        sel = int(selection)
        if 0 < sel < len(queries) + 1:
            return queries[sel-1]['func']
        elif sel == len(queries) + 1:
            return 'finish'
        else:
            return None
    else:
        return None


def ui(context):
    # show emails
    print(context['mails'])
    # require email for login
    email = input('ingrese email para iniciar: ')
    # show initial view
    print(f'bienvenido de nuevo {email}')
    context['email'] = email
    initialLoginView(context)
    # main loop to ask for queries
    stop = False
    while not stop:
        selection = instruction_menu()
        if not selection:
            continue
        elif selection == 'finish':
            stop = True
            continue
        else:
            selection(context)


if __name__ == "__main__":
    connection = happybase.Connection('localhost',32794)
    families = {
        'creation': dict(),
        'edition': dict(),
        'name': dict()
    }
    context = {
        'table': connection
    }
    ui(context)
