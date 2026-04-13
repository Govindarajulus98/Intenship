import socket
import json

def process_task(task):
    try:
        if "task_type" not in task or "data" not in task:
            return "Invalid task format"

        if task["task_type"] == "sum":
            return sum(task["data"])

        elif task["task_type"] == "reverse":
            return task["data"][::-1]

        elif task["task_type"] == "prime":
            n = task["data"]
            if n < 2:
                return False
            for i in range(2, int(n**0.5)+1):
                if n % i == 0:
                    return False
            return True

        else:
            return "Unknown task"

    except Exception as e:
        return f"Error: {str(e)}"

def start_worker():
    worker = socket.socket()
    worker.connect(("localhost", 5000))

    # Register as worker
    worker.send("WORKER".encode())

    print("Worker started...")

    while True:
        try:
            data = worker.recv(1024).decode()

            if not data:
                break

            task = json.loads(data)
            result = process_task(task)

            worker.send(str(result).encode())

        except Exception as e:
            print("Worker error:", e)
            break

    worker.close()


start_worker()