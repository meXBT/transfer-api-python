# meXBT Transfer API Python client

This is a lightweight Python client for the [meXBT](https://mexbt.com) Transfer API. It doesn't try and do anything clever with the JSON response from the API, it simply returns it as-is.

## Install

    pip install mexbt_transfer_api


## Setup

To connect to the production API:

```python
from mexbt_transfer_api import TransferAPI
api = TransferAPI('your_api_key', 'your_api_secret', 123)
```

To connect to the testing API (using bitcoin testnet):

```python
from mexbt_transfer_api import TransferAPI
api = TransferAPI('your_api_key', 'your_api_secret', 123, 'https://transfer-staging.mexbt.com/v1')
```


## Using

```python
api.ping()
api.create_order('btc', 'mxn', 'atm', 'https://your.webhook.com', out_amount=1000,
  sender_info={'name': 'Joe Bloggs', 'email': 'test@test.com'}, recipient_info={'phone': '+52 12345678', 'phone_carrier': 'movistar'})
api.get_order(123)
api.modify_order(123, {'sender_info': {'name': 'Jane Doe'}})

```
