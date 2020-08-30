
def get_connection_uri():
    hostname = 'localhost'
    port = 49161
    sid = 'xe'
    username = 'system'
    password = 'oracle'
    # return f'oe/{username}@{hostname}:{port}/{sid}'
    return (username, password, f'{hostname}:{port}/{sid}')