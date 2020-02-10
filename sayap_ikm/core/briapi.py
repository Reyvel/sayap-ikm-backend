import hmac
import hashlib
import base64
import json
import requests
import random
from datetime import datetime

KEY = 'fymsaLuOFiHcgTA2o0ldGn93TaDLbXcm'
SECRET = 'GUkEZArnxBGtpMVA'
INSTITUTION_CODE = 'J104408'

def get_bri_timestamp():
    timestamp = datetime.utcnow()
    return timestamp.isoformat()[:-3] + 'Z'

def get_bri_token():
    url = 'https://partner.api.bri.co.id/oauth/client_credential/accesstoken?grant_type=client_credentials'
    payload = {'client_id': KEY, 'client_secret': SECRET}
    resp = requests.post(url, data=payload)
    return 'Bearer ' + resp.json()['access_token']


def get_bri_signature(path, verb, token, timestamp, body):
    payload = 'path=' + path + '&verb=' + verb + '&token=' + token + '&timestamp=' \
        + timestamp + '&body=' + json.dumps(body)
    # payload = json.dumps(body)
    maker = hmac.new(
        bytearray(SECRET, encoding='utf-8'),
        bytearray(payload, encoding='utf-8'),
        digestmod=hashlib.sha256
    )
    signature = base64.b64encode(maker.digest())
    return signature


def create_briva(timestamp, token, signature, body):
    url = 'https://partner.api.bri.co.id/sandbox/v1/briva'
    resp = requests.post(
        url,
        headers={
            'BRI-Timestamp': timestamp,
            'BRI-Signature': signature,
            'Authorization': token
        },
        json=body
    )

    return resp.json()


def update_briva(timestamp, token, signature, body):
    url = 'https://partner.api.bri.co.id/sandbox/v1/briva'
    resp = requests.put(
        url,
        headers={
            'BRI-Timestamp': timestamp,
            'BRI-Signature': signature,
            'Authorization': token
        },
        json=body
    )

    return resp.json()


def delete_briva(timestamp, token, signature, body):
    url = 'https://partner.api.bri.co.id/sandbox/v1/briva'
    resp = requests.delete(
        url,
        headers={
            'BRI-Timestamp': timestamp,
            'BRI-Signature': signature,
            'Authorization': token,
            'Content-Type': 'text/plain'
        },
        data=body
    )

    print(resp.json(), resp.request.body, resp.request.headers)
    return resp.json()


def delete_order(user):
    timestamp = get_bri_timestamp()
    token = get_bri_token()

    body = {
        'institutionCode': "J104408",
        'brivaNo': '77777',
        'custCode': str(user.id)
    }

    signature = get_bri_signature(
        '/sandbox/v1/briva',
        'DELETE',
        token,
        timestamp,
        body
    )

    delete_briva(timestamp, token, signature, body)


def create_order(user, amount):
    timestamp =  get_bri_timestamp()
    token = get_bri_token()
    customer_code = random.randint(0, 999999999999) 
    user.customer_code = str(customer_code)
    user.save()

    body = {
            "institutionCode": "J104408",
            "brivaNo": "77777",
            "custCode": str(customer_code),
            "nama": user.first_name + ' ' + user.last_name,
            "amount": amount,
            "keterangan": "",
            "expiredDate": "2020-03-15 09:57:26"
    }

    signature = get_bri_signature(
        '/sandbox/v1/briva',
        'POST',
        token,
        timestamp,
        body
    )

    return create_briva(timestamp, token, signature, body)

