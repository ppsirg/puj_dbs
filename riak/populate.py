
"""
2 cargue datos suficientes para las pruebas

- users: set with all keys of all users
- user_{user_id}: map with user_id data, must have a field follow_to with
  a set of key users that user follows
- {user_id}_tweets: set with keys of all tweets made
- {user_id}_{timestamp}: map with composed name of user_id and timestamp,
  with content, and is_replica_to optional, if exists, contains key of original message
- tweet_origin: map that contains as keys all cities and as values counters 
"""
from random import randint
from datetime import datetime, timedelta

# define network data
users = 100
msg_per_user = 100
max_replies_per_user = 5
max_followers = 10



def populate_data():
    cities = {}
    users = []
