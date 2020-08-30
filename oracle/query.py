# query.py

import cx_Oracle
from connection import get_connection_uri
# Establish the database connection
uri = get_connection_uri()
with cx_Oracle.connect(*uri) as connection:
    print(connection, type(connection))
    # Obtain a cursor
    cursor = connection.cursor()
