from faker import Faker
from datetime import datetime, timedelta
from random import randint, choice
from franz.openrdf.rio.rdfformat import RDFFormat
fk = Faker()

def check_data(conn, filepath):
    """
    import data from file in turtle format
    """
    conn.add(filepath,format=RDFFormat.TURTLE)


def get_hst():
    jb = fk.job()
    ini = jb.split(' ')[0]
    return f'#{ini}'

def get_tm():
    tm = datetime.now() - timedelta(days=randint(0,100))
    return tm.strftime('%Y-%m-%dT%H:%M:%S')

dts = {
    'Message': {
        'prop': {
            'content': fk.text, 
            'hashtag': get_hst,
            'date': get_tm
            }
        },
    'Person': {
        'prop': {
            'name': fk.name,
            'userid': fk.email,
            'country': fk.country
        }
    }
}


def gen_user_message():
    """
    Fast generator of data
    """
    for n,vl in dts.items():
        for i in range(50):
            print(f'res:{n}{i+1} rdf:type class:{n} .')
            for pr,fn in vl['prop'].items():
                print(f'res:{n}{i+1} prop:{pr} {fn()} .')