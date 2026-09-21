# cria e sobe a aplicação Flask

from flask import Flask
from src.route.api import registrar_rotas

app = Flask(__name__)

registrar_rotas(app)

@app.route('/')
def hello_world():  # put application's code here
    return 'Hello World!'


if __name__ == '__main__':
    app.run(debug=True)
