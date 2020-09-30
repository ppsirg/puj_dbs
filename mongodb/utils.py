#-*- coding: utf-8 -*-
import os
import json
from pymongo import MongoClient
from pprint import pprint
from faker import Faker
from random import randint, choices
from datetime import datetime, timedelta

fake = Faker(['es_ES', 'es_MX', 'en_US', 'en_GB', 'pt_BR'])

num_cities = 20
num_users = 100
max_follows = 15
min_follows = 4
format_timestamp = '%Y/%m/%d_%H:%M:%S:%f'
MESSAGE_TYPES = ['ORIGINAL', 'REPLY', 'SHARE']


cities = [fake.city() for a in range(num_cities)]
mails = [fake.email() for a in range(num_users)]


def persist(filename, data):
    with open(f'{filename}.txt', 'w') as fl:
        fl.write(json.dumps(data))


def generate_data():
    user_list = []
    user_keys = []
    for mail in mails:
        key = f'user_{mail}'
        user = {
            'username': mail.split('@')[0], 'email': mail, 
            'city': choices(cities)[0], 
            'following': choices(mails, k=randint(min_follows, max_follows)),
            'publicUser': randint(0,5) == 3,
            'mobile': {'number': fake.phone_number(), 'prefix': fake.country_calling_code()}
        }
        user_list.append(user)
        user_keys.append(key)
    persist('general', {'cities': cities, 'mails': mails})
    persist('users', dict(zip(user_keys, user_list)))


    message_list = []
    message_key_list = []
    for user in user_list:
        timestamp = datetime.now() - timedelta(days=randint(0,100))
        key = f'msg_{user["email"]}_{timestamp.strftime(format_timestamp)}'
        message = {
            'timestamp': timestamp.strftime(format_timestamp),
            'content': fake.text(),
            'messageType': MESSAGE_TYPES[1],
            'owner': f'user_{user["email"]}'
        }
        message_list.append(message)
        message_key_list.append(key)
        if randint(0,5) == 2:
            replicant = choices(mails)[0]
            replytime = timestamp + timedelta(minutes=randint(1,100))
            key_reply = f'msg_{replicant}_{replytime.strftime(format_timestamp)}'
            message_reply = {
                'timestamp': replytime.strftime(format_timestamp),
                'content': fake.text(),
                'messageType': MESSAGE_TYPES[1],
                'owner': f'user_{replicant}',
                'messageBase': key
            }
            message_list.append(message_reply)
            message_key_list.append(key_reply)
        if randint(0,5) == 2:
            replicant = choices(mails)[0]
            sharetime = timestamp + timedelta(minutes=randint(1,100))
            key_share = f'msg_{replicant}_{sharetime.strftime(format_timestamp)}'
            message_share = {
                'timestamp': sharetime.strftime(format_timestamp),
                'content': '',
                'messageType': MESSAGE_TYPES[2],
                'owner': f'user_{replicant}',
                'messageBase': key
            }
            message_list.append(message_share)
            message_key_list.append(key_share)
    persist('messages', dict(zip(message_key_list, message_list)))


def populate(context):
    dirs = os.listdir('.')
    files_exists = [f'{name}.txt' in dirs for name in ['general', 'users', 'messages']]
    if not all(files_exists):
        generate_data()
    db = context['db']
    populated = db.users.find_one({'cities': {'$exists': True}})
    with open('general.txt') as gf:
        raw = gf.read()
        data = json.loads(raw)
    if not populated:
        db.users.insert_one(data)
        with open('users.txt') as uf:
            raw = uf.read()
            users_data = json.loads(raw)
        db.users.insert_many([v for k,v in users_data.items()])
        with open('messages.txt') as mg:
            raw = mg.read()
            messages_data = json.loads(raw)
        db.application.insert_many([v for k,v in messages_data.items()])
    return data['mails']


if __name__ == "__main__":
    client = MongoClient()
    db = client['tallerMongo']
    context = {
        'db': db
    }
    mails = populate(context)
    print(mails)

client = MongoClient()
db = client['tallerMongo']