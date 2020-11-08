from fastapi import FastAPI
from franz.openrdf.connect import ag_connect
from populate import check_data
from queries import search


app = FastAPI()

conn = ag_connect('repo', host='allegrograph-db', port=10035, user='admin', password='pass')
check_data(conn, 'data.txt')


@app.get('/list/hashtag/{hashtag}')
def list_hashtag(hashtag:str):
    """
    Listar todos los mensajes de un hashtag dado en orden cronológico.
    """
    query = """SELECT ?s ?p ?o { 
        ?s ?p ?o . }
    """
    data = search(conn, query, ['s', 'p', 'o'])
    return data


@app.get('/list/messages/{usr}')
def list_messages(usr:str):
    """
    Listar los  mensajes  que  un  usuario  dado puso  desde  el  
    1º de  mayo de  2018  y, en caso  de  haber recibido réplicas 
    a esos mensajes, el texto de las réplicas
    """
    query = """SELECT ?s ?p ?o { 
        ?s ?p ?o . }
    """
    data = search(conn, query, ['s', 'p', 'o'])
    return data


@app.get('/related_countries')
def list_related_countries():
    """
    Listar los países de los usuarios que han hecho retweet 
    de los mensajes que han puesto usuarios que viven en Colombia
    """
    query = """SELECT ?s ?p ?o { 
        ?s ?p ?o . }
    """
    data = search(conn, query, ['s', 'p', 'o'])
    return data


@app.get('/followers/{usr}')
def get_followers(usr:str):
    """
    Encontrar la cadena de seguidores de un usuario dado, es decir, 
    los seguidores del usuario, los seguidores de sus seguidores, 
    los seguidores de los seguidores de sus seguidores, etc
    """
    query = """SELECT ?s ?p ?o { 
        ?s ?p ?o . }
    """
    data = search(conn, query, ['s', 'p', 'o'])
    return data


@app.get('/get_origin/{msg}')
def get_origin(msg:str):
    """
    Encontrar el  origen de un  tweet que fue  re-enviado varias 
    veces, dada una de  las ocurrencias del  reenvío. Listar la 
    fecha del tweet original y el nombre del usuario que lo generó. 
    Tener en cuenta que el retweet puede ser  en varios  niveles,  
    es  decir el  Usuario A pone  el  tweet, el usuario  B hace el  
    retweet, el usuario  C  hace retweet del retweet del usuario B, 
    y así sucesivamente. En ese caso se considera que B y C hicieron 
    retweet del tweet puesto por el usuario A, por lo tanto, el 
    origen es el tweet que puso el usuario A.
    """
    query = """SELECT ?s ?p ?o { 
        ?s ?p ?o . }
    """
    data = search(conn, query, ['s', 'p', 'o'])
    return data


@app.on_event("shutdown")
def shutdown_event():
    conn.close()