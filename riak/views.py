from models import User, Cities
from pprint import pprint


def get_own_msg(user_email):
    """  1.a
    Los últimos 10 mensajes que el usuario ha publicado, 
    en orden cronológico, empezando por el más  reciente.
    Si son réplicas,indica el  mensaje original y  el  
    usuario que lo  publicó. Si  son mensajes re-enviados, 
    indica el usuarioque publicó el mensaje original.
    """
    usr = User(user_email)
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
    usr = User(user_email)
    influencers = usr.info.data['following']
    influencers.sort()
    for followed_email in influencers:
        influencer = User(followed_email)
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
    ranking = Cities.get_ranking(15)