from models import User, Cities
from pprint import pprint
from riak import RiakClient
from argparse import ArgumentParser


cl = RiakClient(protocol='http', host='127.0.0.1', http_port=8098)


def get_own_msg(user_email):
    """  1.a
    Los últimos 10 mensajes que el usuario ha publicado, 
    en orden cronológico, empezando por el más  reciente.
    Si son réplicas,indica el  mensaje original y  el  
    usuario que lo  publicó. Si  son mensajes re-enviados, 
    indica el usuarioque publicó el mensaje original.
    """
    usr = User(cl, user_email)
    last_messages = usr.get_last_messages(10)
    for msg in last_messages:
        if msg['messageType'] == 'ORIGINAL':
            print(msg['timestamp'])
            print(msg['content'])
        elif msg['messageType'] == 'REPLY':
            print(msg['timestamp'])
            print(msg['content'])
            print('reply to ', msg['messageBase']['ref'].split('_')[0])
            print(msg['messageBase']['content'])
        elif msg['messageType'] == 'SHARE':
            print('shared on ', msg['timestamp'])
            print('from ', msg['messageBase']['ref'].split('_')[0])
            print(msg['messageBase']['content'])


def get_follower_msg(user_email):
    """ 1.b
    Los últimos 5 mensajes que han publicado cada uno de
    los usuarios a los que sigue, agrupados por el usuario 
    que los publica. Los usuarios deben estar en orden 
    alfabético y, los mensajes de cada usuario,en orden 
    cronológico,empezando por el más reciente
    """
    usr = User(cl, user_email)
    print('yey')
    influencers = usr.info.data['following']
    print('miau')
    influencers.sort()
    print(influencers)
    for followed_email in influencers:
        influencer = User(cl, followed_email)
        print(influencer.info.data['email'])
        last_messages = influencer.get_last_messages(5)
        for msg in last_messages:
            print(msg['messageType'], ' at ', msg['timestamp'])
            print(msg['content'])


def city_ranking():
    """ 4 
    Realice un ranking de las ciudades por el número de 
    tweets que han producido los usuarios de esa ciudad
    """
    locations = Cities(cl)
    ranking = locations.get_ranking(15)
    pprint(ranking)
    return ranking


def main():
    """
    3 Implemente una aplicación sencilla en algún lenguaje de programación, 
    que permita listar los datos que se refieren en el punto 1
    """
    examples = [
        'isa08@gmail.com',
        'flawson@gmail.com',
        'nllano@castro.es',
        'rivasdolores@industrias.com',
        'stephenswendy@lopez.com',
        'vcantero@yahoo.com',
        'wramos@hotmail.com',
        'imunoz@hotmail.com',
        'hudsontony@gmail.com',
    ]
    stop = False
    print('some data to test: ', examples)
    print('type 0 for exit')
    print('type 1 to get user messages')
    print('type 2 to get user following messages')
    print('type 3 for get city ranking')
    while not stop:
        point = input('point to run ')
        if int(point) == 0:
            stop = True
            break
        elif int(point) == 1:
            user_email = input('put user email ')
            get_own_msg(user_email)
        elif int(point) == 2:
            user_email = input('put user email ')
            get_follower_msg(user_email)
        elif int(point) == 3:
            city_ranking()
        else:
            continue


if __name__ == "__main__":
    main()