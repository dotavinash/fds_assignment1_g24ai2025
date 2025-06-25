from flask import Flask, request, jsonify
import threading
import time
import os

app = Flask(__name__)

# 🧠 Local key-value store and vector clock
data_store = {}
vector_clock = {"node1": 0, "node2": 0, "node3": 0}
NODE_NAME = os.environ.get("NODE_NAME", "node1")

# 🕒 Buffer for delayed messages
message_buffer = []
lock = threading.Lock()

# ✅ Causal readiness check
def is_causally_ready(sender_clock, sender):
    print(f"[{NODE_NAME}] 🧠 Checking causal readiness for: {sender_clock} vs local: {vector_clock}")
    for node in vector_clock:
        if node == sender:
            if sender_clock[node] != vector_clock[node] + 1:
                print(f"[{NODE_NAME}] ❌ Not ready: {node} expected {vector_clock[node]+1}, got {sender_clock[node]}")
                return False
        else:
            if sender_clock[node] > vector_clock[node]:
                print(f"[{NODE_NAME}] ❌ Not ready: {node} clock too far ahead")
                return False
    print(f"[{NODE_NAME}] ✅ Causally ready")
    return True

# ✅ Apply write: update clock and store key
def apply_write(msg):
    key = msg['key']
    value = msg['value']
    sender_clock = msg['clock']

    for node in vector_clock:
        vector_clock[node] = max(vector_clock[node], sender_clock.get(node, 0))

    data_store[key] = value
    vector_clock[NODE_NAME] += 1

    print(f"[{NODE_NAME}] ✅ Stored {key} = {value} | Vector Clock: {vector_clock}")

# 🔄 Periodically check buffer
def buffer_monitor():
    while True:
        time.sleep(2)
        print(f"[{NODE_NAME}] 🌀 Checking buffer...")
        with lock:
            ready_msgs = []
            for msg in message_buffer:
                if is_causally_ready(msg['clock'], msg['sender']):
                    print(f"[{NODE_NAME}] ⏳ Delivering buffered: {msg}")
                    apply_write(msg)
                    ready_msgs.append(msg)
            for m in ready_msgs:
                message_buffer.remove(m)

# 📬 Write endpoint
@app.route('/write', methods=['POST'])
def write():
    print(f"[{NODE_NAME}] 🔔 Received /write request")
    msg = request.get_json()
    with lock:
        if is_causally_ready(msg['clock'], msg['sender']):
            apply_write(msg)
            return jsonify({"status": "stored", "clock": vector_clock}), 200
        else:
            message_buffer.append(msg)
            print(f"[{NODE_NAME}] 🚫 Buffered (not ready): {msg}")
            return jsonify({"status": "buffered", "clock": vector_clock}), 202

# 🔍 Read endpoint
@app.route('/read', methods=['GET'])
def read():
    key = request.args.get("key")
    return jsonify({key: data_store.get(key, None)})

# 🏠 Root
@app.route('/')
def home():
    return f"Hello from {NODE_NAME}. Clock: {vector_clock}"

# 🚀 Start buffer monitor thread
if __name__ == '__main__':
    thread = threading.Thread(target=buffer_monitor, daemon=True)
    thread.start()
    app.run(host='0.0.0.0',port=5000)