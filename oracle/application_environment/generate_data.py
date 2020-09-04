"""
- usuarios que se sigan entre ellos
- usuarios que tengan mensajes, replicas y shares
- usuarios con correos malos
- usuarios y tweets desde hace 6 años
"""
from connection import *
import cx_Oracle
from faker import Faker
from random import randint, choices
from datetime import datetime, timedelta
fake = Faker(['es_ES', 'es_MX', 'en_US', 'en_GB', 'pt_BR'])

q_insert = {
    'countries': "INSERT INTO PUJLAB.COUNTRY VALUES (:cod_country, :name_country)",
    'cities': "INSERT INTO PUJLAB.CITY VALUES (:id_city, :country_cod_country, :name_city)",
    'messages': "INSERT INTO PUJLAB.MESSAGE VALUES (:message_id, :content, :message_owner_id, :reply_to_id, :shared_message_id, :created_date)",
    'network': 'INSERT INTO PUJLAB." SOCIAL_NETWORK" VALUES (:user_id, :user_id_related, :relation_type, :created_date)',
    'user': 'INSERT INTO PUJLAB."USER" VALUES (:id_user, :city_id_city, :email, :mobile, :mobile_prefix, :passwd, :public_profile, :user_name, :created_date)',
    'topic_hashtag': "INSERT INTO PUJLAB.TOPIC_HASHTAG VALUES (:topic_content, :message_message_id)",
}

q_search = 'select * from PUJLAB.{}'

hashtags = [
    'mises', 'hayek', 'rothbard', 'huertaDeSoto', 'rayo',
    'milei', 'echebarne', 'carrino', 'kaiser', 'giacomini',
    'danan', 'tipitoEnojado', 'paralelo33', 'eldolarcito',
    'libertad', 'propiedad', 'emprendimiento', 'libertario',
    'impuestos', 'censura', 'regulacion', 'robo'
    ]


def countries_gen():
    with open('countries.csv', 'r') as fl:
        dialect = csv.Sniffer().sniff(fl.read(1024))
        fl.seek(0)
        data = csv.DictReader(fl, dialect=dialect)
        for a in data:
            if a['cd3']:
                yield a['cd3'], a['name']
            else:
                break


def cities_gen():
    c_gen = countries_gen()
    c_codes = [c[0] for c in c_gen]
    for i in range(500):
        # :id_city, :country_cod_country, :name_city
        yield [i, choices(c_codes)[0], fake.city()]


def email_gen():
    while True:
        if randint(1,9) == 3:
            # bad email
            yield fake.name()
        else:
            yield fake.email()


def date_gen(rn=[0,4]):
    current = datetime.now()
    last_gen = datetime.now()
    while True:
        last_gen = current - timedelta(randint(*rn))
        yield last_gen
        current = last_gen


def users_gen():
    mail_g = email_gen()
    date_g = date_gen()
    for i in range(3000):
        # :id_user, :city_id_city, :email, 
        # :mobile, :mobile_prefix, 
        # :passwd, :public_profile, :user_name, :created_date
        yield [
            i, choices(range(400))[0], mail_g.__next__(), 
            choices(range(1111111111,8888888888))[0], choices(range(111,888))[0],
            fake.password(), randint(1,9) < 7, fake.name(), date_g.__next__()
            ]


def msg_gen(users, conn):
    # :message_id, :content, :message_owner_id, :reply_to_id, :shared_message_id, :created_date
    stop = False
    count = 30
    max_len_fake_text = 138 - max([len(a) for a in hashtags])
    now = datetime.now()
    for u in users:
        replies_prom = randint(1,4)
        try:
            q = f'SELECT * FROM PUJLAB." SOCIAL_NETWORK" WHERE user_id_related=:user_id_related'
            d = [u[0]]
            actual_follows = search_in_db(conn, q, d=d)
        except Exception as err:
            print(err)
            continue
        dt = u[8]
        while dt < now:
            # message
            tag = '#{}'.format(*choices(hashtags))
            text = fake.text()
            if len(text) > max_len_fake_text:
                text = text[:max_len_fake_text] + tag
            else:
                text += tag
            msg = [
                count, text, u[0], None, None, dt
            ]
            hsh = [tag, count]
            yield msg, hsh
            count += 1
            for rp in choices(actual_follows, k=replies_prom):
                # replies
                tag = '#{}'.format(*choices(hashtags))
                text = fake.text()
                if len(text) > max_len_fake_text:
                    text = text[:max_len_fake_text] + tag
                else:
                    text += tag
                msg = [
                    count, text, rp[0], count - 1, None, max(dt, rp[3])
                ]
                hsh = [tag, count]
                yield msg, hsh
                count += 1
            dt += timedelta(randint(7, 100))


def gen_network(users, conn):
    # user_id following user_id_related
    # :user_id, :user_id_related, :relation_type, :created:date
    st = False
    for u in users:
        if st:
            q = f'SELECT * FROM PUJLAB." SOCIAL_NETWORK" WHERE user_id_related=:user_id_related'
            d = [u[0]]
            actual_follows = search_in_db(conn, q, d=d)
            actual_follows = [a[0] for a in actual_follows]
        else:
            actual_follows = []
        to_follow = [a for a in choices(users, k=randint(5, 7)) if a != u and a not in actual_follows]
        for rel in to_follow:
            dt = max(u[8], rel[8]) + timedelta(randint(0,3))
            if rel[6] == '0':
                # private
                yield [u[0], rel[0], 'FOLLOWING', dt]
                yield [rel[0], u[0], 'FOLLOWING', dt]
            else:
                # public
                yield [rel[0], u[0], 'FOLLOWING', dt]


def bench():
    uri = get_connection_uri()
    db_pool = cx_Oracle.SessionPool(*uri, min=2, max=5, increment=1)
    conn = db_pool.acquire()
    # data generation
    q = f'SELECT * FROM PUJLAB."USER"' # can be deleted
    users = search_in_db(conn, q) # can be deleted
    msg_g = msg_gen(users, conn)
    for msg, hsh in msg_g:
        write_in_db(conn, q_insert['messages'], msg)
        if hsh:
            write_in_db(conn, q_insert['topic_hashtag'], hsh)
    q = f"SELECT * FROM PUJLAB.MESSAGE"
    search_in_db(conn, q)
    q = f"SELECT * FROM PUJLAB.TOPIC_HASHTAG"
    search_in_db(conn, q)
    # connection delete
    db_pool.release(conn)
    db_pool.close()
    

def populate():
    uri = get_connection_uri()
    db_pool = cx_Oracle.SessionPool(*uri, min=2, max=5, increment=1)
    conn = db_pool.acquire()
    cursor = conn.cursor()
    # data generation
    # --------------------------------
    # countries
    datagen = countries_gen()
    for cd, nm in datagen:
        cursor.execute(q_insert['countries'], [cd, nm])
    conn.commit()
    q = f"SELECT * FROM PUJLAB.COUNTRY"
    print(search_in_db(conn, q))
    # cities
    dg = cities_gen()
    for c in dg:
        cursor.execute(q_insert['cities'], c)
    conn.commit()
    q = f"SELECT * FROM PUJLAB.CITY"
    print(search_in_db(conn, q))
    # q = f"SELECT * FROM PUJLAB.COUNTRY
    # user
    dg = users_gen()
    for data in dg:
        print(data)
        cursor.execute(q_insert['user'], data)
    conn.commit()
    q = f'SELECT * FROM PUJLAB."USER"'
    users = search_in_db(conn, q)
    print(users)
    users = choices(users, k=1000)
    # network
    net_g = gen_network(users, conn)
    for msg in net_g:
        cursor.execute(q_insert['network'], msg)
    conn.commit()
    q = f'SELECT * FROM PUJLAB." SOCIAL_NETWORK"'
    print(search_in_db(conn, q))
    # messages
    msg_g = msg_gen(users, conn)
    count = 0
    for msg, hsh in msg_g:
        cursor.execute(q_insert['messages'], msg)
        if hsh:
            cursor.execute(q_insert['topic_hashtag'], hsh)
        conn.commit()
        count += 1
    q = f"SELECT * FROM PUJLAB.MESSAGE"
    print(search_in_db(conn, q))
    q = f"SELECT * FROM PUJLAB.TOPIC_HASHTAG"
    print(search_in_db(conn, q))
    # topic_hashtag
    # --------------------------------
    # connection delete
    db_pool.release(conn)
    db_pool.close()


if __name__ == "__main__":
    populate()