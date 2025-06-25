from flask import Flask, request
import requests
import re

app = Flask(__name__)

SUBSTATIONS = ['http://substation1:5002', 'http://substation2:5002']

def get_current_load(url):
    try:
        resp = requests.get(f"{url}/metrics")
        match = re.search(r'substation_load\s+(\d+)', resp.text)
        return int(match.group(1)) if match else float('inf')
    except:
        return float('inf')

@app.route('/route', methods=['POST'])
def route_request():
    best_station = min(SUBSTATIONS, key=get_current_load)
    resp = requests.post(f"{best_station}/charge")
    return resp.json(), resp.status_code

if __name__ == '__main__':
    app.run(host='0.0.0.0',port=5001)