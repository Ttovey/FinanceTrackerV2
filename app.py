from plaid.api import plaid_api
from plaid.model.link_token_create_request import LinkTokenCreateRequest
from plaid.model.link_token_create_request_user import LinkTokenCreateRequestUser
from plaid.model.item_public_token_exchange_request import ItemPublicTokenExchangeRequest
from plaid.model.transactions_get_request import TransactionsGetRequest
from plaid.model.transactions_get_request_options import TransactionsGetRequestOptions
from plaid.model.products import Products
from plaid.model.accounts_get_request import AccountsGetRequest
from plaid.model.country_code import CountryCode
from flask import Flask, render_template, jsonify, json
import plaid
import os
import datetime

app = Flask(__name__)

PLAID_CLIENT_ID = os.environ.get(
    'PLAID_CLIENT_ID')
PLAID_SECRET = os.environ.get('PLAID_SECRET')


configuration = plaid.Configuration(
    host=plaid.Environment.Development,
    api_key={
        'clientId': PLAID_CLIENT_ID,
        'secret': PLAID_SECRET,
    }
)

api_client = plaid.ApiClient(configuration)
client = plaid_api.PlaidApi(api_client)

access_token = None
item_id = None


@app.route('/')
def index():
    return render_template('index.html')


@app.route("/create_link_token", methods=['POST'])
def create_link_token():
    # Get the client_user_id by searching for the current user
    # user = User.find(...)
    client_user_id = '1'

    # Create a link_token for the given user
    request = LinkTokenCreateRequest(
        products=[Products("auth")],
        client_name="Plaid Test App",
        country_codes=[CountryCode('US')],
        language='en',
        webhook='https://webhook.example.com',
        user=LinkTokenCreateRequestUser(
                client_user_id=client_user_id
        )
    )
    response = client.link_token_create(request)

    # Send the data to the client
    return jsonify(response.to_dict())


@app.route('/exchange_public_token', methods=['POST'])
def exchange_public_token():
    from flask import request
    global access_token
    public_token = request.form['public_token']
    request = ItemPublicTokenExchangeRequest(
        public_token=public_token
    )
    response = client.item_public_token_exchange(request)
    access_token = response['access_token']
    item_id = response['item_id']
    print(access_token)
    print(item_id)
    return jsonify(response.to_dict())

# Retrieve an Item's accounts


@app.route('/accounts', methods=['GET'])
def get_accounts():
    print(access_token)
    print(item_id)
    try:
        request = AccountsGetRequest(
            access_token=access_token
        )
        accounts_response = client.accounts_get(request)
    except plaid.ApiException as e:
        response = json.loads(e.body)
        return jsonify({'error': {'status_code': e.status, 'display_message':
                        response['error_message'], 'error_code': response['error_code'], 'error_type': response['error_type']}})
    return jsonify(accounts_response.to_dict())


@app.route('/plaid/transactions', methods=['GET'])
def get_transactions():
    # Pull transactions for the last 30 days
    start_date = (datetime.datetime.now() - datetime.timedelta(days=30))
    end_date = datetime.datetime.now()
    try:
        options = TransactionsGetRequestOptions()
        request = TransactionsGetRequest(
            access_token=access_token,
            start_date=start_date.date(),
            end_date=end_date.date(),
            options=options
        )
        response = client.transactions_get(request)
        print(response.to_dict())
        return response.to_dict()
    except plaid.ApiException as e:

        return e


if __name__ == "__main__":
    app.run(port=8000, debug=True)
