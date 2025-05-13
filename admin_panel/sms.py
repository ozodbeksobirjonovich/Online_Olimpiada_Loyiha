import hashlib
import time
import requests

username = "-----"
secretkey = "--------"


def send_sms(phone, message):
    url = "https://routee.sayqal.uz/sms/TransmitSMS"
    utime = int(time.time())
    token = hashlib.md5(" ".join(["TransmitSMS", username, secretkey, str(utime)]).encode('utf-8')).hexdigest()

    sms = {
        "utime": utime,
        "username": username,
        "service": {
            "service": 2
        },
        "message": {
            "smsid": 1,
            "phone": phone,
            "text": message
        }
    }

    try:
        response = requests.post(url, json=sms, headers={"Content-Type": "application/json", "X-Access-Token": token}, )
        if response.status_code == 200:
            pass
    except Exception as ex:
        print("Error")
