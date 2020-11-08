from fastapi import FastAPI
from franz.openrdf.connect import ag_connect


app = FastAPI()


@app.get('/')
def inicial():
    """
    docstring
    """
    return {'db': 'allegro'}


def make_connection(parameter_list):
    """
    docstring
    """    
    with ag_connect(
        'repo', host='localhost', port=10035,
        user='admin', password='pass') as conn:
        print(conn.size())
        import pdb; pdb.set_trace()
