from flask import Flask, jsonify, request
from waitress import serve

from scrapper.banco_chile import BancoChile



app = Flask(__name__)


@app.route('/api/banco-chile/recipients', methods=['POST'])
def banco_chile_recipients():
    username = request.json["username"]
    password = request.json["password"]
    entity = BancoChile(username, password)
    entity.login()
    return jsonify(entity.recipients())


@app.route('/api/banco-chile/transactions', methods=['POST'])
def banco_chile_transactions():
    username = request.json["username"]
    password = request.json["password"]
    entity = BancoChile(username, password)
    entity.login()
    return jsonify(entity.transactions())


@app.route('/api/banco-chile/products', methods=['POST'])
def banco_chile_products():
    username = request.json["username"]
    password = request.json["password"]
    entity = BancoChile(username, password)
    entity.login()
    return jsonify(entity.products())


@app.route('/api/banco-chile/cards', methods=['POST'])
def banco_chile_cards():
    username = request.json["username"]
    password = request.json["password"]
    entity = BancoChile(username, password)
    entity.login()
    return jsonify(entity.products())


@app.route('/api/banco-chile/profile', methods=['POST'])
def banco_chile_profile():
    username = request.json["username"]
    password = request.json["password"]
    entity = BancoChile(username, password)
    entity.login()
    return jsonify(entity.profile())


@app.route('/api/banco-chile/userdata', methods=['POST'])
def banco_chile_userdata():
    username = request.json["username"]
    password = request.json["password"]
    entity = BancoChile(username, password)
    entity.login()
    return jsonify(entity.userdata())


def is_port_in_use(port):
    import socket
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        return s.connect_ex(('localhost', port)) == 0


def run_server(_port=5000):
    serve(app, host='0.0.0.0', port=_port)


if __name__ == '__main__':
    port = 5000
    if not is_port_in_use(port):
        # app.run(debug=True)
        run_server(port)
    else:
        print("port 5000 is already in use, see ya ;)")
