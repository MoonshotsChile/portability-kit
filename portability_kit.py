import os
from flask import Flask, jsonify, request
from flask_cors import CORS
from waitress import serve
from src.banco_chile import BancoChile
from src.exceptions import LoginFailedException

app = Flask(__name__)
CORS(app)


@app.route('/portability-kit/banco-chile/recipients', methods=['POST'])
def banco_chile_recipients():
    username = request.json["username"]
    password = request.json["password"]
    entity = BancoChile(username, password)
    entity.login()
    return jsonify(entity.recipients())


@app.route('/portability-kit/banco-chile/transactions', methods=['POST'])
def banco_chile_transactions():
    username = request.json["username"]
    password = request.json["password"]
    entity = BancoChile(username, password)
    entity.login()
    return jsonify(entity.transactions())


@app.route('/portability-kit/banco-chile/products', methods=['POST'])
def banco_chile_products():
    username = request.json["username"]
    password = request.json["password"]
    entity = BancoChile(username, password)
    entity.login()
    return jsonify(entity.products())


@app.route('/portability-kit/banco-chile/cards', methods=['POST'])
def banco_chile_cards():
    username = request.json["username"]
    password = request.json["password"]
    entity = BancoChile(username, password)
    entity.login()
    return jsonify(entity.products())


@app.route('/portability-kit/banco-chile/profile', methods=['POST'])
def banco_chile_profile():
    username = request.json["username"]
    password = request.json["password"]
    entity = BancoChile(username, password)
    entity.login()
    return jsonify(entity.profile())


@app.route('/portability-kit/banco-chile/userdata', methods=['POST'])
def banco_chile_userdata():
    username = request.json["username"]
    password = request.json["password"]
    entity = BancoChile(username, password)
    entity.login()
    return jsonify(entity.userdata())


@app.route('/portability-kit/banco-chile/sessionkey', methods=['POST'])
def banco_chile_sessionkey():
    username = request.json["username"]
    password = request.json["password"]
    entity = BancoChile(username, password)
    entity.login()
    return entity.session_key()


@app.route('/portability-kit/banco-chile/bills', methods=['POST'])
def banco_chile_bills():
    username = request.json["username"]
    password = request.json["password"]
    entity = BancoChile(username, password)
    entity.login()
    return jsonify(entity.registered_bills())


@app.errorhandler(LoginFailedException)
def handle_login_failed(error):
    response = jsonify(error.to_dict())
    response.status_code = error.status_code
    return response


@app.errorhandler(ValueError)
def handle_value_error(error):
    response = jsonify(error.to_dict())
    response.status_code = error.status_code
    return response


def is_port_in_use(port):
    import socket
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        return s.connect_ex(('localhost', port)) == 0


def run_server(_port=5000):
    serve(app, host='0.0.0.0', port=_port)


if __name__ == '__main__':
    port = 5000
    if os.environ.get("PYTHON_ENV") == "prod":
        if not is_port_in_use(port):
            run_server(port)
        else:
            print(f"port {port} is already in use, see ya ;)")
    else:
        app.run(debug=True)
