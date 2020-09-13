
"""
2 cargue datos suficientes para las pruebas

- users_set: set with all keys of all users
- user_{user_id}: map with user_id data, must have a field follow_to with
  a set of key users that user follows
- {user_id}_tweets: set with keys of all tweets made
- {user_id}_{timestamp}: map with composed name of user_id and timestamp,
  with content, and is_replica_to optional, if exists, contains key of original message
"""
from riak import RiakClient
from random import randint
from faker import Faker
from datetime import datetime, timedelta
from riak.datatypes import Set, Counter, Map

fake = Faker(['es_ES', 'es_MX', 'en_US', 'en_GB', 'pt_BR'])


# define network data
num_users = 500
num_cities = 50
msg_per_user = 100
max_replies_per_user = 5
max_followers = 10


class RiakBase(object):

    def __init__(self):
        self.client = RiakClient(protocol='http', host='127.0.0.1', http_port=8098)


class User(RiakBase):
    INDEX_BUCKET = 'users_set'
    BUCKET = '{}_tweets'

    def __init__(self, id):
        super().__init__(self)
        self.id = id
        self.info_bucket = self.client.bucket('users')
        self.msg_bucket = self.client.bucket(f'{self.id}_messages')

    def add_message(self, message):
        pass

    def follow_user(self, user_to_follow_id):
        pass

    def populate(self):
        keys = self.info_bucket.get_keys()
        if len(keys.data) == :
            for usr_id in range(num_users):
                self.info_bucket.new(f'usr_{usr_id}', {'email': fake.email(), 'follow_to':[]})



class Message(RiakBase):
    pass


class Cities(RiakBase):
    """Dictionary of cities with city associated
    to number of tweets in ranking
    """
    BUCKET = 'cities'

    def __init__(self):
        super().__init__(self)
        self.bucket = self.client.bucket(self.BUCKET)

    def populate(self):
        keys = self.bucket.get_keys()
        if self.BUCKET not in keys.data:
            cities_list = {fake.city(): 0 for a in range(num_cities)}
            cities = self.bucket.new(self.BUCKET, cities_list)
            cities.store()

    def increment(self, city):
        value = self.bucket.get(self.BUCKET)
        value.data[city] += 1
        value.store()

    def get_ranking(self, num):
        cities = self.bucket.get(self.BUCKET).data
        rank = [(k,v) for k,v in cities.items()]
        rank.sort(key=lambda x: x[1])
        return rank[:num]