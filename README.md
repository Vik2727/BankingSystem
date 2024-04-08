## Simple Banking System API

This is a simple banking system API implemented using Python and Flask. It allows users to create accounts, deposit money, withdraw money, and transfer money between accounts. The API also includes JWT token-based authentication for secure access.

### Installation

1. Clone this repository:

    ```
    git clone https://github.com/Vik2727/BankingSystem.git
    ```

2. Navigate to the project directory:

    ```
    cd bankingsystem
    ```

3. Install the required dependencies from the `requirements.txt` file:

    ```
    pip install -r requirements.txt
    ```

### Usage

1. Run the Flask server:

    ```
    python banking.py
    ```

2. Once the server is running, you can send requests to the API endpoints using tools like Postman or cURL.

### Testing

To run the unit tests, navigate to the project directory and execute the following command:

    ```
    python -m unittest tests.py
    ```

### API Endpoints

#### 1. Create Account

- **Endpoint**: `/create_account`
- **Method**: POST
- **Parameters**:
  - `name`: Name of the account holder (string)
  - `initial_balance`: Initial balance of the account (float)
- **Response**: JSON response with the newly created account details including an account ID and an access token.

#### 2. Deposit Funds

- **Endpoint**: `/deposit`
- **Method**: POST
- **Parameters**:
  - `account_id`: ID of the account to deposit to (integer)
  - `amount`: Amount to deposit (float)
- **Authentication**: JWT token required
- **Response**: JSON response with updated account balance.

#### 3. Withdraw Funds

- **Endpoint**: `/withdraw`
- **Method**: POST
- **Parameters**:
  - `account_id`: ID of the account to withdraw from (integer)
  - `amount`: Amount to withdraw (float)
- **Authentication**: JWT token required
- **Response**: JSON response with updated account balance.

#### 4. Transfer Funds

- **Endpoint**: `/transfer`
- **Method**: POST
- **Parameters**:
  - `from_account_id`: ID of the account to transfer from (integer)
  - `to_account_id`: ID of the account to transfer to (integer)
  - `amount`: Amount to transfer (float)
- **Authentication**: JWT token required
- **Response**: JSON response with updated balances of both accounts involved in the transfer.

### Error Handling

The API handles cases where accounts do not exist, do not have sufficient funds, or the user has insufficient access rights. Appropriate error messages and status codes are returned in such cases.

### Additional Features

- JWT token-based authentication for secure access.
- Support for multiple currencies.
- Logging for transactions.
- Rate limiting to prevent abuse.

### Contributing

Contributions are welcome! Please feel free to open an issue or submit a pull request with any improvements or additional features.

### License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
