
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
num_users = 200
num_cities = 50
msg_per_user = 30
max_replies_per_user = 5
max_followers = 10
format_timestamp = '%Y/%m/%d_%H:%M:%S:%f'
MESSAGE_TYPES = ['ORIGINAL', 'REPLY', 'SHARE']


class RiakBase(object):

    def __init__(self):
        self.client = RiakClient(protocol='http', host='127.0.0.1', http_port=8098)


class Cities():
    """Manage cities to calculate cities ranking of tweets.
    """
    BUCKET = 'citiesY'

    def __init__(self, cl):
        self.client = cl
        self.bucket = self.client.bucket(self.BUCKET)
        # check if data
        keys = self.bucket.get(self.BUCKET)
        if keys:
            self.value = self.bucket.get(self.BUCKET)
        else:
            cities_list = {f'{fake.city()}': 0 for a in range(num_cities)}
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


class User():
    INFO_BUCKET = 'users'
    MSG_BUCKET = 'tweet'
    LAST_BUCKET = 'tweet_last10'

    def __init__(self, cl, email, city=None):
        self.client = cl
        self.repr = f'user_{email}'
        self.cities = Cities(self.client)
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
        owner_info = {k:v for k,v in self.info.data.items() if k != 'following'}
        message_body = {
            'timestamp': timestamp,
            'content': message,
            'messageType': (MESSAGE_TYPES[1] if message else MESSAGE_TYPES[2]) if reply_to else MESSAGE_TYPES[0],
            'owner': owner_info
        }
        if reply_to:
            message_body['messageBase'] = reply_to
        # save message
        messages_list = self.msg_bucket.get(self.repr)
        if not messages_list.data:
            messages_list = self.msg_bucket.new(
                self.repr,
                {'messages': [message_body]}
                )
            
        else:
            messages_list.data['messages'].insert(0, message_body)
        messages_list.store()
        # update cities counter
        self.cities.increment(self.info.data['city'])
        # update last messages bucket
        self.last_messages.data['data'].insert(0, message_body)
        if len(self.last_messages.data['data']) == 11:
            self.last_messages.data['data'].pop()
        self.last_messages.store()
        return message_body

    def get_last_messages(self, num):
        last_messages = self.last_messages.data
        if num >= 10:
            return last_messages.get('data')
        else:
            return last_messages.get('data')[:num]

    def follow_user(self, user_to_follow_id):
        self.info.data['following'].append(user_to_follow_id)
        self.info.store()


def populate():
    cl = RiakClient(protocol='http', host='127.0.0.1', http_port=8098)
    cities = Cities(cl)
    users_list = []
    # create users
    print('doing users')
    for i in range(num_users):
        usr = User(cl, fake.email())
        users_list.append(usr)
        print(usr.info.data)
    # make users follow each others
    print('doing follows')
    for usr in users_list:
        to_follow = choices(users_list, k=10)
        for tg in to_follow:
            usr.follow_user(tg.repr)
        print(usr.info.data)
    # create messages
    print('doing messages')
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
            print('original', new_msg)
            if random_pick == 2:
                # its a replica
                replicant = choices(users_list)[0]
                reply_timestamp = current + timedelta(minutes=randint(3, 90))
                original_msg_ref = '_'.join([new_msg['owner']['email'], new_msg['timestamp']])
                new_reply = replicant.add_message(
                    fake.text(), 
                    timestamp=reply_timestamp.strftime(format_timestamp),
                    reply_to={
                        'ref': original_msg_ref, 
                        'content': new_msg['content']
                        }
                )
                print('reply', new_reply)
            elif random_pick == 3:
                # its a share
                replicant = choices(users_list)[0]
                reply_timestamp = current + timedelta(minutes=randint(3, 90))
                original_msg_ref = '_'.join([new_msg['owner']['email'], new_msg['timestamp']])
                new_reply = replicant.add_message(
                    '', 
                    timestamp=reply_timestamp.strftime(format_timestamp),
                    reply_to={
                        'ref': original_msg_ref, 
                        'content': new_msg['content']
                        }
                )
                print('share', new_reply)
    
if __name__ == "__main__":
    populate()