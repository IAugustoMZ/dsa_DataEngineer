import time
import redis
from flask import Flask

# cria a aplicação flask
app = Flask(__name__)

# conecta no host do Redis
cache = redis.Redis(host='dsadb', port=6379)

# cria uma função para contagem de acessos
def get_hit_count():
    retries = 5
    while True:
        try:
            return cache.incr('hits')
        except redis.exceptions.ConnectionError as exc:
            if retries == 0:
                raise exc
            retries -= 1
            time.sleep(0.5)

# cria a rota raiz com a função hello
@app.route('/')
def hello():

    # obtém a contagem
    contador = get_hit_count()

    # verifica o contador
    if contador == 1:
        contagem = 'Sucesso Icaro! Esta página foi acessada {} vez.\n'.format(contador)
    else:
        contagem = 'Sucesso Icaro! Esta página foi acessada {} vezes.\n'.format(contador)

    return contagem

