#!/usr/bin/python3.4

import random
import httplib2
import time
import urllib.parse

apiKey = "U9CL7Y7ZUNN7CTLL"
url = "https://api.thingspeak.com/update"


def doit():
    value = random.randint(1, 100)
    rawValue = random.randint(1, 1000)

    body = urllib.parse.urlencode({'api_key': apiKey,
                                   'field1': value,
                                   'field2': rawValue})

    headers = {"Content-type": "application/x-www-form-urlencoded", "Accept": "text/plain"}

    response, content = httplib2.Http().request(url, "POST", body, headers)

    if content == b'0':
        print("failed")
    else:
        print('success')


while True:
    doit()
    time.sleep(16)
