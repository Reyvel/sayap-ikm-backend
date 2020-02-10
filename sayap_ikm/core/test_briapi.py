import briapi
from datetime import datetime

class User:
    pass

user = User()
user.id = 1
briapi.delete_order(user)

body = {
            "institutionCode": "J104408",
            "brivaNo": "77777",
            "custCode": "467976160498",
            "nama": "Septri Nur",
            "amount": "1000000",
            "keterangan": "",
            "expiredDate": "2020-03-15 09:57:26"
        }
token = briapi.get_bri_token()
timestamp = briapi.get_bri_timestamp()

signature = briapi.get_bri_signature(
        '/sandbox/v1/briva',
        'POST',
        token,
        timestamp,
        body
    )

print(briapi.create_briva(timestamp, token, signature, body))