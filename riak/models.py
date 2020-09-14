
"""
2 cargue datos suficientes para las pruebas

"""
from riak import RiakClient
from random import randint, choices
from faker import Faker
from datetime import datetime, timedelta
from hashlib import blake2b
from riak.datatypes import Set, Counter, Map

fake = Faker(['es_ES', 'es_MX', 'en_US', 'en_GB', 'pt_BR'])


# define network data
num_users = 500
num_cities = 50
msg_per_user = 100
max_replies_per_user = 5
max_followers = 10
format_timestamp = '%Y/%m/%d_%H:%M:%S:%f'


class RiakBase(object):

    def __init__(self):
        self.client = RiakClient(protocol='http', host='127.0.0.1', http_port=8098)


class Cities(RiakBase):
    """Manage cities to calculate cities ranking of tweets.
    """
    BUCKET = 'cities'

    def __init__(self):
        super().__init__(self)
        self.bucket = self.client.bucket(self.BUCKET)
        # check if data
        keys = self.bucket.get_keys()
        if self.BUCKET in keys:
            self.value = self.bucket.get(self.BUCKET)
        else:
            cities_list = {f'{fake.language()} {fake.city()}': 0 for a in range(num_cities)}
            cities = self.bucket.new(self.BUCKET, cities_list)
            cities.store()
            self.value = cities

    @property
    def _list(self):
        return [k for k,v in self.value.data.items()]

    def increment(self, city):
        value = self.bucket.get(self.BUCKET)
        value.data[city] += 1
        value.store()

    @property
    def get_ranking(self, num):
        rank = [(k,v) for k,v in self.value.data.items()]
        rank.sort(reverse=True, key=lambda x: x[1])
        return rank[:num]


class User(RiakBase):
    INFO_BUCKET = 'users'
    MSG_BUCKET = '{}_messages'

    def __init__(self, id, email=None, city=None):
        super().__init__(self)
        self.id = id
        self.repr = f'user_{id}'
        self.cities = Cities()
        self.info_bucket = self.client.bucket(self.INFO_BUCKET)
        self.msg_bucket = self.client.bucket(self.MSG_BUCKET.format(self.id))
        info = self.info_bucket.get(self.repr)
        if not info.data:
            self.email = email if email else fake.email()
            self.city = city if city else choices(self.cities._list)[0]
            self.info = self.info_bucket.new(
                self.repr, 
                {'id': self.id, 'email': self.email, 'city': self.city, 'following_to': []}
                )
            self.info.store()
        else:
            self.info = info

    def add_message(self, message, reply_to=None, timestamp=None):
        timestamp = datetime.now().strftime(format_timestamp) if not timestamp else timestamp
        msg_hash = blake2b(message.encode(encoding='utf-8'), digest_size=10)
        msg_id = f'{timestamp}__{msg_hash.hexdigest()}'
        message_body = {
            'id': msg_id
            'content': message,
        }
        if reply_to:
            message_body['reply_to'] = reply_to
        new_msg = self.msg_bucket.new(msg_id, message_body)
        new_msg.store()
        self.cities.increment(self.info.data['city'])
        return new_msg

    def get_last_messages(self, num):
        msgs = [[a, a.split('__')] for a in self.msg_bucket.get_keys()]
        msgs.sort(reverse=True, key=lambda x: datetime.strptime(x[1][0], format_timestamp))
        return msgs[:num]

    def follow_user(self, user_to_follow_id):
        self.info['following_to'].append(user_to_follow_id)
        self.info.store()


def populate():
    cities = Cities()
    users_list = []
    # create users
    for i in range(num_users):
        usr = User(i, fake.email())
        users_list.append(usr)
    # make users follow each others
    for usr in users_list:
        to_follow = choices(users_list, k=10)
        for tg in to_follow:
            usr.follow_user(tg.repr)
    # create messages
    for usr in users_list:
        num_msg = randint(5, msg_per_user)
        current = datetime.now()
        for msg in range(num_msg):
            current -= timedelta(randint(1, 10))
            new_msg = usr.add_message(
                fake.text(),
                timestamp=current.strftime(format_timestamp)
                )
            # figure out if make a share or a replica out of this
            random_pick = randint(0,5)
            if random_pick == 2:
                # its a replica
                replicant = choices(users_list)[0]
                reply_timestamp = current + timedelta(minutes=randint(3, 90))
                new_reply = replicant.add_message(
                    fake.text(), 
                    timestamp=reply_timestamp.strftime(format_timestamp),
                    reply_to=new_msg.data['id']
                )
            elif random_pick == 3:
                # its a share
                replicant = choices(users_list)[0]
                reply_timestamp = current + timedelta(minutes=randint(3, 90))
                new_reply = replicant.add_message(
                    '', 
                    timestamp=reply_timestamp.strftime(format_timestamp),
                    reply_to=new_msg.data['id']
                )
    