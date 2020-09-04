

def get_connection_uri():
    """
    pujlab, clave: Pujlab123!, ip: 127.0.0.1, puerto: 1521
    """
    hostname = '127.0.0.1'
    port = 1521
    sid = 'xe'
    username = 'pujlab'
    password = 'Pujlab123!'
    return (username, password, f'{hostname}:{port}/{sid}')


def search_in_db(conn, q, d=None):
    print(q, d)
    cursor = conn.cursor()
    if d:
        cursor.execute(q, d)
    else:
        cursor.execute(q)
    resp = cursor.fetchall()
    return resp


def write_in_db(conn, q, d):
    print(q, d)
    cursor = conn.cursor()
    cursor.execute(q, d)
    return conn.commit()