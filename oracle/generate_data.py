"""
- usuarios que se sigan entre ellos
- usuarios que tengan mensajes, replicas y shares
- usuarios con correos malos
- usuarios y tweets desde hace 6 años
"""
from faker import Faker
from random import randint, choices
from datetime import datetime, timedelta
fake = Faker(['es_ES', 'en_US'])


def create_users():
    for i in range(20):
        user_name = fake.name()
        email = 
        mobile =
        mobile_prefix =
        passwd
        public_profile
        print(f'{i};{name};{address};{text}')


def create_tweets():
    pass