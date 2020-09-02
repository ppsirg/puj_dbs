

def get_connection_uri():
    """
    pujlab, clave: Pujlab123!, ip: 127.0.0.1, puerto: 1521
    """
    hostname = 'oracle-db'
    port = 1521
    sid = 'xe'
    username = 'pujlab'
    password = 'Pujlab123!'
    return (username, password, f'{hostname}:{port}/{sid}')


def search_in_db(db_pool, query):
    connection = db_pool.acquire()
    cursor = connection.cursor()
    if query:
        resp = cursor.execute(query)
    else:
        resp = {'data': None}
    db_pool.release(connection)
    return resp