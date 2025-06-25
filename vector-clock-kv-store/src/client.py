import requests
import time

nodes = {
    "node1": "http://localhost:5001",
    "node2": "http://localhost:5002",
    "node3": "http://localhost:5003"
}

# Simulated vector clock
vc1 = {"node1": 1, "node2": 0, "node3": 0}  # Valid for node1
vc2 = {"node1": 2, "node2": 0, "node3": 0}  # Ahead of what node2 expects

def write_to_node(node_name, key, value, clock, sender):
    payload = {
        "key": key,
        "value": value,
        "clock": clock,
        "sender": sender
    }
    print(f"\n🟢 Writing {key}={value} to {node_name} with VC={clock}")
    response = requests.post(nodes[node_name] + "/write", json=payload)
    print(f"Response: {response.text}")

def read_from_node(node_name, key):
    print(f"\n🔵 Reading key '{key}' from {node_name}")
    response = requests.get(nodes[node_name] + f"/read?key={key}")
    print(f"Response: {response.text}")

# STEP 1: Write valid message to node1
write_to_node("node1", "fruit", "apple", vc1, "node1")
time.sleep(1)

# STEP 2: Write "too early" message to node2 (should get buffered)
write_to_node("node2", "fruit", "banana", vc2, "node1")
time.sleep(1)

# STEP 3: Read from both
read_from_node("node1", "fruit")
read_from_node("node2","fruit")