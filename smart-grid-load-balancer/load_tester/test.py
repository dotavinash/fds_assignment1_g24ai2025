import requests

url = "http://localhost:5000/request_charge"

for _ in range(100):
    try:
        response = requests.post(url)
        print(response.status_code, response.json())
    except Exception as e:
        print(response.status_code, "Error:", e, "| Raw Response:",response.text)