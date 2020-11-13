import os
from fastapi import FastAPI
from franz.openrdf.connect import ag_connect
from populate import check_data
from queries import search


app = FastAPI()

host = 'allegrograph-db' if os.getenv('WAIT_HOSTS') else 'localhost'

conn = ag_connect('try1', host=host, port=10035, user='admin', password='pass')
check_data(conn, 'data.txt')


@app.get('/list/hashtag/{hashtag}')
def list_hashtag(hashtag:str):
    """
    Listar todos los mensajes de un hashtag dado en orden cronológico.
    """
    query = """prefix  res:   <http://example.com/resource/>
        prefix  ex:    <http://example.com/>
        prefix  class: <http://example.com/class/>
        prefix  prop:  <http://example.com/property/>
        prefix  rdf:   <http://www.w3.org/1999/02/22-rdf-syntax-ns#>

        SELECT ?message ?txt ?ht ?dt WHERE {
        ?message rdf:type class:Message. 
        ?message prop:content ?txt. 
        ?message prop:hashtag ?ht.
        ?message prop:date ?dt 
        FILTER( ?ht = "#--hashtag--")}

    ORDER BY DESC(?dt)
    """
    data = search(conn, query.replace('--hashtag--', hashtag), ['message', 'txt', 'ht', 'dt'])
    return data


@app.get('/list/messages/{usr}')
def list_messages(usr:str):
    """
    Listar los  mensajes  que  un  usuario  dado puso  desde  el  
    1º de  mayo de  2018  y, en caso  de  haber recibido réplicas 
    a esos mensajes, el texto de las réplicas
    """
    query = """prefix  res:   <http://example.com/resource/>
        prefix  ex:    <http://example.com/>
        prefix  class: <http://example.com/class/>
        prefix  prop:  <http://example.com/property/>
        prefix  rdf:   <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
        
        SELECT ?message ?id ?person ?dt ?txt ?reply ?txtRp WHERE {
            ?message rdf:type class:Message.
            ?person rdf:type class:Person.
            ?message prop:owner ?person.
            ?person prop:userid ?id.
            ?message prop:date ?dt.
            OPTIONAL{?message prop:content ?txt}.
            OPTIONAL{?message prop:reply ?reply.
                    ?reply prop:content ?txtRp}.
            FILTER( 
                ?dt > xsd:dateTime("2018-01-24T00:00:40") &&
                ?id = "--user--"
                    )}
    """
    data = search(
        conn, 
        query.replace('--user--', usr), 
        ['message', 'id', 'person', 'dt', 'txt', 'reply', 'txtRp']
        )
    return data


@app.get('/related_countries')
def list_related_countries():
    """
    Listar los países de los usuarios que han hecho retweet 
    de los mensajes que han puesto usuarios que viven en Colombia
    """
    query = """prefix  res:   <http://example.com/resource/>
        prefix  ex:    <http://example.com/>
        prefix  class: <http://example.com/class/>
        prefix  prop:  <http://example.com/property/>
        prefix  rdf:   <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
        SELECT ?user_origin ?country_origin ?country_reply ?message_origin WHERE {
            ?message rdf:type class:Message.
            ?reply rdf:type class:Message.
            ?person rdf:type class:Person.
            ?preply rdf:type class:Person.
            ?message prop:owner ?person.
            ?message prop:content ?message_origin.
            ?person prop:userid ?user_origin.
            ?person prop:country ?country_origin.
            ?message prop:reply ?reply.
            ?reply prop:owner ?preply.
            ?preply prop:country ?country_reply
            FILTER ( ?country_origin="Colombia")
        }
    """
    data = search(conn, query, ['user_origin', 'country_origin', 'country_reply', 'message_origin'])
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