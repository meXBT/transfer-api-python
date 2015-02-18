import json
import hmac
import time
import hashlib

import requests

class TransferAPI:
    def __init__(self, api_key, api_secret, client_id, endpoint="https://transfer.mexbt.com/v1"):
        self.api_key = api_key
        self.api_secret = api_secret
        self.client_id = client_id
        self.endpoint = endpoint

    def get_auth_params(self):
        nonce = int(time.time() * 10000)
        signature = hmac.HMAC(
                key=self.api_secret.encode(),
                msg=('%s%s%s' % (nonce, self.client_id, self.api_key)).encode(),
                digestmod=hashlib.sha512).hexdigest().upper()
        return {
                'api_key': self.api_key,
                'nonce': nonce,
                'signature': signature,
                }

    def make_call(self, path, params={}):
        url = '%s/%s' % (self.endpoint, path)
        auth_params = self.get_auth_params()
        merged_params = {}
        merged_params.update(params)
        merged_params.update(auth_params)
        headers = {
                'content-type': 'application/json',
                'accept': 'json'
                }
        res = requests.post(url, data=json.dumps(merged_params), headers=headers, verify=True, timeout=20)
        try:
            json_response = res.json()
        except:
            json_response = None
        if res.status_code != 200:
            if json_response and json_response['error']:
                raise Exception(json_response['error'])
            else:
                raise Exception('Unknown error calling API (%s): %s' % (res.status_code, res.text))

        return json_response

    def ping(self):
        return self.make_call(path='ping')

    def get_order(self, order_id):
        path = 'orders/%s' % order_id
        return self.make_call(path=path)

    def create_order(self, in_currency, out_currency, out_via, webhook,
            in_amount=0, out_amount=0, sender_info={}, recipient_info={},
            skip_deposit_address_setup=False):
        """
        Create an order
        """

        params = {
                'in_currency': in_currency,
                'out_currency': out_currency,
                'out_via': out_via,
                'webhook': webhook,
                'sender_info': sender_info,
                'recipient_info': recipient_info,
                'skip_deposit_address_setup': skip_deposit_address_setup,
                }

        if in_amount > 0:
            params['in'] = in_amount
        elif out_amount > 0:
            params['out'] = out_amount
        else:
            raise Exception("You must specify a value for either in or out")

        return self.make_call("orders", params=params)

    def modify_order(self, order_id, modifications_dict):
        """
        Modify an order_id with modifications_dict

        modifications_dict should only contain changes, don't repost the original info
        """

        assert order_id and modifications_dict
        assert type(order_id) is int
        assert type(modifications_dict) is dict

        VALID_KEYS = (
                'sender_info',
                'recipient_info',
                'out',
                'setup_deposit_address',
                )
        for k in modifications_dict:
            assert k in VALID_KEYS, k

        uri = 'orders/%s/modify' % order_id

        return self.make_call(uri, params=modifications_dict)
