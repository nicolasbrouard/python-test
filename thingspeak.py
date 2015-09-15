import random
import httplib2
import time

apiKey = "U9CL7Y7ZUNN7CTLL"
url = "https://api.thingspeak.com/update"
conn = httplib2.Http()

def doit():
    value = random.randint(1, 100)
    rawValue = random.randint(1, 1000)
    request = conn.request(url, "POST", "api_key=" + apiKey + "&field1=%d&field2=%d" %(value, rawValue))
    print(request)
    print(request[0]['status'])
    body = request[1]
    if body == b'0':
        print("failed")
    else:
        print('success')

while True:
    doit()
    time.sleep(16)

