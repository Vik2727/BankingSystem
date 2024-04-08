import unittest
from banking import app, accounts
from unittest.mock import patch
from flask_jwt_extended import create_access_token


class TestCreateAccountEndpoint(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()

    @patch('banking.create_access_token')
    def test_create_account_success(self, mock_create_access_token):
        mock_create_access_token.return_value = 'fake_token'
        data = {
            'name': 'John Doe',
            'initial_balance': 100
        }
        response = self.app.post('/create_account', json=data)
        self.assertEqual(response.status_code, 201)
        response_data = response.get_json()
        self.assertIn('account_id', response_data)
        self.assertEqual(response_data['name'], 'John Doe')
        self.assertEqual(response_data['balance'], 100)
        self.assertEqual(response_data['access_token'], 'fake_token')

    def test_create_account_missing_parameters(self):
        response = self.app.post('/create_account', json={})
        self.assertEqual(response.status_code, 400)


class TestDepositEndpoint(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        self.jwt_token = self.get_jwt_token()
        self.setup_test_data()

    def get_jwt_token(self):
        with app.test_request_context():
            access_token = create_access_token(identity=1)
            return access_token

    def setup_test_data(self):
        accounts[2] = {
            'name': 'Test User',
            'balance': 1000.0
        }

    def test_deposit_with_valid_data(self):
        data = {
            "account_id": 1,
            "amount": 100
        }
        response = self.app.post('/deposit', json=data, headers={'Authorization': f'Bearer {self.jwt_token}'})
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"new_balance", response.data)

    def test_deposit_invalid_account_id(self):
        data = {
            "account_id": 999,
            "amount": 100
        }
        response = self.app.post('/deposit', json=data, headers={'Authorization': f'Bearer {self.jwt_token}'})
        self.assertEqual(response.status_code, 404)
        self.assertIn(b"The account does not exist", response.data)

    def test_deposit_negative_amount(self):
        data = {
            "account_id": 1,
            "amount": -100
        }
        response = self.app.post('/deposit', json=data, headers={'Authorization': f'Bearer {self.jwt_token}'})
        self.assertEqual(response.status_code, 400)
        self.assertIn(b"The sum must be greater than 0", response.data)

    def test_deposit_insufficient_access(self):
        data = {
            "account_id": 2,
            "amount": 100
        }
        response = self.app.post('/deposit', json=data, headers={'Authorization': f'Bearer {self.jwt_token}'})
        self.assertEqual(response.status_code, 403)
        self.assertIn(b"Insufficient access rights for this account", response.data)


class TestWithdrawEndpoint(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        self.jwt_token = self.get_jwt_token()
        self.setup_test_data()

    def get_jwt_token(self):
        with app.test_request_context():
            access_token = create_access_token(identity=1)
            return access_token

    def setup_test_data(self):
        accounts[1] = {
            'name': 'Test User',
            'balance': 1000.0
        }

    def test_withdraw_with_valid_data(self):
        data = {
            "account_id": 1,
            "amount": 100
        }
        response = self.app.post('/withdraw', json=data, headers={'Authorization': f'Bearer {self.jwt_token}'})
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"new_balance", response.data)

    def test_withdraw_invalid_account_id(self):
        data = {
            "account_id": 999,
            "amount": 100
        }
        response = self.app.post('/withdraw', json=data, headers={'Authorization': f'Bearer {self.jwt_token}'})
        self.assertEqual(response.status_code, 404)
        self.assertIn(b"The account does not exist", response.data)

    def test_withdraw_negative_amount(self):
        data = {
            "account_id": 1,
            "amount": -100
        }
        response = self.app.post('/withdraw', json=data, headers={'Authorization': f'Bearer {self.jwt_token}'})
        self.assertEqual(response.status_code, 400)
        self.assertIn(b"The sum must be greater than 0", response.data)

    def test_withdraw_insufficient_funds(self):
        data = {
            "account_id": 1,
            "amount": 2000
        }
        response = self.app.post('/withdraw', json=data, headers={'Authorization': f'Bearer {self.jwt_token}'})
        self.assertEqual(response.status_code, 400)
        self.assertIn(b"There are insufficient funds in the account", response.data)

    def test_withdraw_insufficient_access(self):
        data = {
            "account_id": 2,
            "amount": 100
        }
        response = self.app.post('/withdraw', json=data, headers={'Authorization': f'Bearer {self.jwt_token}'})
        self.assertEqual(response.status_code, 403)
        self.assertIn(b"Insufficient access rights for this account", response.data)


class TestTransferEndpoint(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        self.jwt_token = self.get_jwt_token()
        self.setup_test_data()

    def get_jwt_token(self):
        with app.test_request_context():
            access_token = create_access_token(identity=1)
            return access_token

    def setup_test_data(self):
        accounts[1] = {'name': 'Test User 1', 'balance': 1000.0}
        accounts[2] = {'name': 'Test User 2', 'balance': 500.0}

    def test_transfer_with_valid_data(self):
        data = {
            "from_account_id": 1,
            "to_account_id": 2,
            "amount": 100
        }
        response = self.app.post('/transfer', json=data, headers={'Authorization': f'Bearer {self.jwt_token}'})
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"to_account_balance", response.data)

    def test_transfer_invalid_account_id(self):
        data = {
            "from_account_id": 999,
            "to_account_id": 2,
            "amount": 100
        }
        response = self.app.post('/transfer', json=data, headers={'Authorization': f'Bearer {self.jwt_token}'})
        self.assertEqual(response.status_code, 404)
        self.assertIn(b"One of the accounts does not exist", response.data)

    def test_transfer_negative_amount(self):
        data = {
            "from_account_id": 1,
            "to_account_id": 2,
            "amount": -100
        }
        response = self.app.post('/transfer', json=data, headers={'Authorization': f'Bearer {self.jwt_token}'})
        self.assertEqual(response.status_code, 400)
        self.assertIn(b"The sum must be greater than 0", response.data)

    def test_transfer_insufficient_funds(self):
        data = {
            "from_account_id": 1,
            "to_account_id": 2,
            "amount": 1500
        }
        response = self.app.post('/transfer', json=data, headers={'Authorization': f'Bearer {self.jwt_token}'})
        self.assertEqual(response.status_code, 400)
        self.assertIn(b"There are insufficient funds in the account", response.data)

    def test_transfer_insufficient_access(self):
        data = {
            "from_account_id": 2,
            "to_account_id": 1,
            "amount": 100
        }
        response = self.app.post('/transfer', json=data, headers={'Authorization': f'Bearer {self.jwt_token}'})
        self.assertEqual(response.status_code, 403)
        self.assertIn(b"Insufficient access rights for this account", response.data)


if __name__ == '__main__':
    unittest.main()
