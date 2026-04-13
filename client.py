import socket
import json

def send_task(task):
    client = socket.socket()
    client.connect(("localhost", 5000))

    client.send(json.dumps(task).encode())

    result = client.recv(1024).decode()
    print("Task:", task)
    print("Result:", result)
    print("----------------------")

    client.close()


# READ TASKS FROM FILE
with open("tasks.txt", "r") as f:
    for line in f:
        task = json.loads(line.strip())
        send_task(task)