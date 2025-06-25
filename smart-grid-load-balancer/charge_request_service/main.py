from flask import Flask, request
import requests

app = Flask(__name__)

@app.route('/request_charge', methods=['POST'])
def request_charge():
    response = requests.post("http://load_balancer:6000/route")
    return response.text, response.status_code

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=7000)