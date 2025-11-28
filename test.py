import json
import zmq

def client():
    # socket setup
    context = zmq.Context()
    socket = context.socket(zmq.REQ)
    socket.connect("tcp://localhost:8932")

    # prep data to send
    test_data = {"title": "my super cool photo", "date": "10-12-2025", "location": "Tessa's house", "notes": "We watched a movie and made pizza"}
    data_str = json.dumps(test_data)

    socket.send_string(data_str)

    response = socket.recv()
    decoded = response.decode()

    print("Generated tag string:", decoded)

    context.destroy()

if __name__ == "__main__":
    client()
