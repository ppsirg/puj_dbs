import pdb
import redis

r = redis.Redis(host='localhost', port=6389, db=0)
r.set('saludo_es', 'hola a todos mis compadres!!!')
response = r.get('saludo_es')
print(response)