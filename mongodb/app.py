import json
from pymongo import MongoClient
from pprint import pprint
from views import initialLoginView
from utils import populate
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
    client = MongoClient()
    db = client['test-database']
    context = {
        'db': db
    }
    # if no data, populate database
    mails = populate()
    context['mails'] = mails
    # run application
    ui(context)