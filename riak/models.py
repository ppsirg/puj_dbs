
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
MESSAGE_TYPES = ['ORIGINAL', 'REPLY', 'SHARE']


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
    MSG_BUCKET = 'tweet'
    LAST_BUCKET = 'tweet_last10'

    def __init__(self, email, city=None):
        super().__init__(self)
        self.repr = f'user_{email}'
        self.cities = Cities()
        # initialize bucket
        self.info_bucket = self.client.bucket(self.INFO_BUCKET)
        self.msg_bucket = self.client.bucket(self.MSG_BUCKET)
        self.last_bucket = self.client.bucket(self.LAST_BUCKET)
        info = self.info_bucket.get(self.repr)
        if not info.data:
            self.email = email if email else fake.email()
            self.city = city if city else choices(self.cities._list)[0]
            self.info = self.info_bucket.new(
                self.repr,
                # structure of user
                {
                    'username': fake.name(), 'email': self.email, 
                    'city': self.city, 'following': [],
                    'publicUser': randint(0,5) == 3,
                    'mobile': {'number': fake.phone_number(), 'prefix': fake.country_calling_code()}
                    }
                )
            self.info.store()
            self.last_messages = self.last_bucket.new(
                self.repr,
                # structure of last messages
                {'data': []}
                )
            self.last_messages.store()
        else:
            self.info = info
            self.last_messages = self.last_bucket.get(self.repr)

    def add_message(self, message, reply_to=None, timestamp=None):
        # build message body
        timestamp = datetime.now().strftime(format_timestamp) if not timestamp else timestamp
        owner_info = {k,v for k,v in self.info.data.items() if k != 'following'}
        message_body = {
            'timestamp': timestamp,
            'content': message,
            'messageType': choices(MESSAGE_TYPES)[0],
            'owner': owner_info
        }
        if reply_to:
            message_body['messageBase'] = reply_to
        # save message
        new_msg = self.msg_bucket.new(msg_id, message_body)
        new_msg.store()
        # update cities counter
        self.cities.increment(self.info.data['city'])
        # update last messages bucket
        self.last_messages.data['data'].insert(message_body)
        if len(self.last_messages.data['data']) == 11:
            self.last_messages.data['data'].pop()
        self.last_messages.store()
        return new_msg

    def get_last_messages(self, num):
        last_messages = self.last_messages.data
        if num >= 10:
            return last_messages.get('data')
        else:
            return last_messages.get('data')[:num]

    def follow_user(self, user_to_follow_id):
        self.info['following'].append(user_to_follow_id)
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
    