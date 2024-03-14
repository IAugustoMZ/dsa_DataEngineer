import os
import json
from flask import Flask, render_template, abort, url_for, json, jsonify

# definição do app
app = Flask(__name__, template_folder='.')

# carrega o arquivo
with open('arquivo.json', 'r') as arquivo_json:
    dados = arquivo_json.read()

# rota
@app.route('/')
def index():
    return render_template('index.html', title='Lab5', jsonfile = json.dumps(dados))

# execução do programa
if __name__ == '__main__':
    app.run(debug=True)