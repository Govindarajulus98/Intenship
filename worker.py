import socket
import json
import time


def process_task(task):

    print("Worker Received:", task)

    time.sleep(5)

    task_type = task.get("task_type")
    data = task.get("data")

    if task_type == "sum":
        return sum(data)

    elif task_type == "reverse":
        return data[::-1]

    elif task_type == "sleep":

        time.sleep(data)

        return f"Slept for {data} seconds"

    return "Task Completed"


def start_worker():

    worker = socket.socket()

    connected = False

    while not connected:

        try:

            worker.connect(("localhost", 5000))

            connected = True

            print("Connected to Server")

        except:

            print("Waiting for server...")

            time.sleep(2)

    worker.send("WORKER".encode())

    print("Worker Started")

    try:

        data = worker.recv(1024).decode()

        if data:

            task = json.loads(data)

            result = process_task(task)

            print("Sending Result:", result)

            worker.send(str(result).encode())

    except Exception as e:

        print("Worker Error:", e)

    worker.close()

    print("Worker Exited")
if __name__ == "__main__":

    start_worker()