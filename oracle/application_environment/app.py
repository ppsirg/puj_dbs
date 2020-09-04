import cx_Oracle
from time import sleep
from connection import get_connection_uri, search_in_db
from typing import Optional
from fastapi import FastAPI
from queries import *


print('launch_service')
uri = get_connection_uri()
for i in range(50):
    try:
        db_pool = cx_Oracle.SessionPool(*uri, min=2, max=5, increment=1)
        sleep(10)
        break
    except Exception as e:
        print(e)
print('doing great')
app = FastAPI()


def fetch_data(query, data=None):
    conn = db_pool.acquire()
    resp = search_in_db(conn, query, d=data)
    db_pool.release(conn)
    return resp


@app.on_event('shutdown')
def release_database_session():
    print('closing connection')
    db_pool.close()
    print('connections closed')


@app.get("/")
def mainView():
    return {"go_to": 'load /docs'}


@app.get("/list/users")
def listUsersView():
    queries = example_query()
    response = {}
    expressions = {}
    for k, query in queries.items():
        response[k] = fetch_data(query)
        expressions[k] = query
    return {
        "query": expressions, 
        'args': None, 
        'response': response
        }


@app.get("/login/{user_id}")
def loginView(user_id: int):
    queries = get_login_data()
    response = {}
    expressions = {}
    for k, query in queries.items():
        response[k] = fetch_data(query, data=[user_id])
        expressions[k] = query
    return {
        "query": expressions, 
        'args': None, 
        'response': response
        }


@app.get("/followers/differential/{user_a_email}/{user_b_email}")
def followerDiffView(user_a_email: int, user_b_email: int):
    queries = get_a_followers_not_in_b()
    response = {}
    expressions = {}
    for k, query in queries.items():
        response[k] = fetch_data(query.format(a=user_a_email, b=user_b_email))
        expressions[k] = query
    return {
        "query": expressions, 
        'args': None, 
        'response': response
        }


@app.get("/user_by_email/")
def userDetailByEmailView():
    queries = get_user_info_from_good_email()
    response = {}
    expressions = {}
    for k, query in queries.items():
        response[k] = fetch_data(query)
        expressions[k] = query
    return {
        "query": expressions, 
        'args': None, 
        'response': response
        }


@app.get("/list_recent_users_tweet/")
def recentTweetView():
    queries = list_users_3_years()
    response = {}
    expressions = {}
    for k, query in queries.items():
        response[k] = fetch_data(query)
        expressions[k] = query
    return {
        "query": expressions, 
        'args': None, 
        'response': response
        }


@app.get("/city_rank/")
def cityRankView():
    queries = get_city_rank_by_tweets()
    response = {}
    expressions = {}
    for k, query in queries.items():
        response[k] = fetch_data(query)
        expressions[k] = query
    return {
        "query": expressions, 
        'args': None, 
        'response': response
        }


@app.get("/followers_tree/{root_name}")
def followerTreeView(root_name: str):
    queries = folowers_tree()
    response = {}
    expressions = {}
    for k, query in queries.items():
        response[k] = fetch_data(query)
        expressions[k] = query
    return {
        "query": expressions, 
        'args': None, 
        'response': response
        }

