from flask import Flask, jsonify, request

from scrapper.banco_chile import BancoChile

app = Flask(__name__)


@app.route('/banco-chile/recipients', methods=['POST'])
def banco_chile_recipients():
    username = request.json["username"]
    password = request.json["password"]
    entity = BancoChile(username, password)
    entity.login()
    return jsonify(entity.recipients())


@app.route('/banco-chile/transactions', methods=['POST'])
def banco_chile_transactions():
    username = request.json["username"]
    password = request.json["password"]
    entity = BancoChile(username, password)
    entity.login()
    return jsonify(entity.transactions())


@app.route('/banco-chile/products', methods=['POST'])
def banco_chile_products():
    username = request.json["username"]
    password = request.json["password"]
    entity = BancoChile(username, password)
    entity.login()
    return jsonify(entity.products())


@app.route('/banco-chile/cards', methods=['POST'])
def banco_chile_cards():
    username = request.json["username"]
    password = request.json["password"]
    entity = BancoChile(username, password)
    entity.login()
    return jsonify(entity.products())


@app.route('/banco-chile/profile', methods=['POST'])
def banco_chile_profile():
    username = request.json["username"]
    password = request.json["password"]
    entity = BancoChile(username, password)
    entity.login()
    return jsonify(entity.profile())


@app.route('/banco-chile/userdata', methods=['POST'])
def banco_chile_userdata():
    username = request.json["username"]
    password = request.json["password"]
    entity = BancoChile(username, password)
    entity.login()
    return jsonify(entity.userdata())


if __name__ == '__main__':
    app.run(debug=True)
