from flask import Flask, request, jsonify
from flask_jwt_extended import JWTManager, jwt_required, create_access_token, get_jwt_identity
from datetime import timedelta


app = Flask(__name__)
app.config['JWT_SECRET_KEY'] = 'super-secret'
jwt = JWTManager(app)

accounts = {}
account_id_counter = 1


# Creating an account with receiving a JWT token
@app.route('/create_account', methods=['POST'])
def create_account():
    global account_id_counter
    data = request.json
    name = data.get('name')
    initial_balance = data.get('initial_balance')
    if name is None or initial_balance is None:
        return jsonify({"error": "Mandatory parameters are missing"}), 400

    account_id = account_id_counter
    accounts[account_id] = {
        'name': name,
        'balance': initial_balance,
        'currency': 'USD'
    }
    account_id_counter += 1

    # Generating a JWT token for a new account
    expires = timedelta(days=7)  # The token is valid for 7 days
    access_token = create_access_token(identity=account_id, expires_delta=expires)

    return jsonify({"account_id": account_id, "name": name, "balance": initial_balance, "access_token": access_token}), 201


# Depositing funds into the account
@app.route('/deposit', methods=['POST'])
@jwt_required()
def deposit():
    data = request.json
    account_id = data.get('account_id')
    amount = data.get('amount')
    current_user_id = get_jwt_identity()

    if account_id not in accounts:
        return jsonify({"error": "The account does not exist"}), 404
    if amount <= 0:
        return jsonify({"error": "The sum must be greater than 0"}), 400
    if account_id != current_user_id:
        return jsonify({"error": "Insufficient access rights for this account"}), 403

    accounts[account_id]['balance'] += amount
    return jsonify({"account_id": account_id, "new_balance": accounts[account_id]['balance']}), 200


# Withdrawal of funds from the account
@app.route('/withdraw', methods=['POST'])
@jwt_required()
def withdraw():
    data = request.json
    account_id = data.get('account_id')
    amount = data.get('amount')
    current_user_id = get_jwt_identity()

    if account_id not in accounts:
        return jsonify({"error": "The account does not exist"}), 404
    if current_user_id != account_id:
        return jsonify({"error": "Insufficient access rights for this account"}), 403
    if amount <= 0:
        return jsonify({"error": "The sum must be greater than 0"}), 400
    if accounts[account_id]['balance'] < amount:
        return jsonify({"error": "There are insufficient funds in the account"}), 400

    accounts[account_id]['balance'] -= amount
    return jsonify({"account_id": account_id, "new_balance": accounts[account_id]['balance']}), 200


# Transfer of funds between accounts
@app.route('/transfer', methods=['POST'])
@jwt_required()
def transfer():
    current_user = get_jwt_identity()
    data = request.json
    from_account_id = data.get('from_account_id')
    to_account_id = data.get('to_account_id')
    amount = data.get('amount')

    if from_account_id not in accounts or to_account_id not in accounts:
        return jsonify({"error": "One of the accounts does not exist"}), 404
    if amount <= 0:
        return jsonify({"error": "The sum must be greater than 0"}), 400
    if accounts[from_account_id]['balance'] < amount:
        return jsonify({"error": "There are insufficient funds in the account"}), 400
    if current_user != from_account_id:
        return jsonify({"error": "Insufficient access rights for this account"}), 403

    accounts[from_account_id]['balance'] -= amount
    accounts[to_account_id]['balance'] += amount
    return jsonify({
        "from_account_id": from_account_id,
        "to_account_id": to_account_id,
        "from_account_balance": accounts[from_account_id]['balance'],
        "to_account_balance": accounts[to_account_id]['balance']
    }), 200


if __name__ == '__main__':
    app.run(debug=True)
