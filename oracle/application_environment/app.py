import cx_Oracle
from connection import get_connection_uri, search_in_db
from typing import Optional
from fastapi import FastAPI
from queries import *


uri = get_connection_uri()
db_pool = cx_Oracle.SessionPool(*uri, min=2, max=5, increment=1)
app = FastAPI()


@app.on_event('shutdown')
def release_database_session():
    print('closing connection')
    db_pool.close()
    print('connections closed')

@app.get("/date")
def dateView(q: Optional[str] = None):
    query = get_fecha_db()
    resp = search_in_db(query)
    print(type(resp), resp)
    return {"item_id": 'some', "q": q}


@app.get("/login/{user_id}")
def loginView(user_id: int, q: Optional[str] = None):
    query = get_login_data(user_id)
    resp = search_in_db(query)
    print(type(resp), resp)
    return {"item_id": 'some', "q": q}


@app.get("/followers/differential/{user_a_email}/{user_b_email}")
def followerDiffView(user_a_id: int, user_b_id: int, q: Optional[str] = None):
    query = get_a_followers_not_in_b(user_a_id, user_b_id)
    resp = search_in_db(query)
    print(type(resp), resp)
    return {"item_id": 'some', "q": q}


@app.get("/user_by_email/{email}")
def userDetailByEmailView(email: str, q: Optional[str] = None):
    query = get_user_info_from_good_email(email)
    resp = search_in_db(query)
    print(type(resp), resp)
    return {"item_id": 'some', "q": q}


@app.get("/list_recent_users_tweet/")
def recentTweetView(q: Optional[str] = None):
    query = list_users_3_years()
    resp = search_in_db(query)
    print(type(resp), resp)
    return {"item_id": 'some', "q": q}


@app.get("/city_rank/")
def cityRankView(q: Optional[str] = None):
    query = get_city_rank_by_tweets()
    resp = search_in_db(query)
    print(type(resp), resp)
    return {"item_id": 'some', "q": q}


@app.get("/followers_tree/{root_email}")
def followerTreeView(root_email: str, q: Optional[str] = None):
    query = folowers_tree()
    resp = search_in_db(query)
    print(type(resp), resp)
    return {"item_id": 'some', "q": q}

