from flask import Flask, request
from prometheus_client import Gauge, generate_latest, CONTENT_TYPE_LATEST

app = Flask(__name__)
load_gauge = Gauge('substation_load', 'Current load on substation')

@app.route('/charge', methods=['POST'])
def charge():
    load_gauge.inc()
    return {'status': 'charging started'}, 200

@app.route('/metrics')
def metrics():
    return generate_latest(), 200, {'Content-Type': CONTENT_TYPE_LATEST}

if __name__ == '__main__':
    start_http_server:(5002)  # for Prometheus
    app.run(host='0.0.0.0', port=5002)
