import requests

payload = {
    "url": "TEST",
    "status_code": "200",
    "timestamp": "2020-01-01 00:00:00",}

def send_request():
    url = 'http://127.0.0.1:5000/oopcqmbblx2y62i7/artundweise/heartbeat'
    headers = {'Content-Type': 'application/json'}

    r = requests.post(url, headers=headers, json=payload)

    if r.status_code == 200:
        print("Success")
    else:
        print("Failure")

send_request()