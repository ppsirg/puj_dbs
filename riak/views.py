from models import User, Cities
from pprint import pprint


def get_own_msg(user_id):
    """  1.a
    Los últimos 10 mensajes que el usuario ha publicado, 
    en orden cronológico, empezando por el más  reciente.
    Si son réplicas,indica el  mensaje original y  el  
    usuario que lo  publicó. Si  son mensajes re-enviados, 
    indica el usuarioque publicó el mensaje original.
    """
    usr = User(user_id)
    last_messages = usr.get_last_messages(10)
    pprint(last_messages)



def get_follower_msg(user_id):
    """ 1.b
    Los últimos 5 mensajes que han publicado cada uno de
    los usuarios a los que sigue, agrupados por el usuario 
    que los publica. Los usuarios deben estar en orden 
    alfabético y, los mensajes de cada usuario,en orden 
    cronológico,empezando por el más reciente
    """
    usr = User(user_id)
    for followed_id in usr.info['following_to']:
        influencer = User(followed_id)
        print(influencer.info['email'])
        pprint(influencer.get_last_messages(5))



def city_ranking():
    """ 4 
    Realice un ranking de las ciudades por el número de 
    tweets que han producido los usuarios de esa ciudad
    """
    ranking = Cities.get_ranking(15)