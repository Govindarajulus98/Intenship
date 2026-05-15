import socket
import threading
import queue
import time
import json

workers = []

worker_locks = []

worker_index = 0

worker_id_counter = 1

client_id_counter = 1

active_tasks = 0

completed_tasks = 0

current_task = None

task_limit = threading.Semaphore(1)

task_queue = queue.Queue()

waiting_tasks_list = []


def update_status():

    data = {
        "workers": len(workers),
        "waiting_tasks": len(waiting_tasks_list),
        "waiting_list": waiting_tasks_list,
        "active_tasks": active_tasks,
        "completed_tasks": completed_tasks,
        "current_task": current_task,
        "server_status": "Running"
    }

    with open("status.json", "w") as f:

        json.dump(data, f)


def process_task(client_socket, data, client_id):

    global worker_index
    global active_tasks
    global completed_tasks
    global current_task

    task_limit.acquire()

    try:

        print("\nProcessing Task:", data)

        if not workers:

            client_socket.send(
                "No worker available".encode()
            )

            return

        current_task = {
            "client": client_id,
            "task": data
        }

        active_tasks += 1

        update_status()

        worker_data = workers[
            worker_index % len(workers)
        ]

        worker = worker_data["socket"]

        worker_id = worker_data["id"]

        lock = worker_locks[
            worker_index % len(workers)
        ]

        worker_index += 1

        print(
            f"{client_id} assigned to {worker_id}"
        )

        with lock:

            worker.send(data.encode())

            result = worker.recv(1024).decode()

        print("Result:", result)

        worker.close()

        workers.remove(worker_data)

        worker_locks.pop(0)

        active_tasks -= 1

        completed_tasks += 1

        current_task = None

        update_status()

        with open("log.txt", "a") as f:

            f.write(
                f"{client_id} -> {worker_id} | "
                f"Task: {data} | "
                f"Result: {result}\n"
            )

        client_socket.send(result.encode())

    except Exception as e:

        print("Error:", e)

    finally:

        task_limit.release()

        client_socket.close()


def queue_worker():

    while True:

        if not task_queue.empty():

            client_socket, data, client_id = (
                task_queue.get()
            )

            print(
                f"Queue Size: {task_queue.qsize()}"
            )

            update_status()

            process_task(
                client_socket,
                data,
                client_id
            )

            if waiting_tasks_list:

                waiting_tasks_list.pop(0)

            update_status()

        time.sleep(0.1)


def handle_client(client_socket, first_message):

    global client_id_counter

    client_id = f"Client-{client_id_counter}"

    client_id_counter += 1

    print(f"{client_id} Connected")

    task_queue.put(
        (
            client_socket,
            first_message,
            client_id
        )
    )

    waiting_tasks_list.append({
        "client": client_id,
        "task": first_message
    })

    print(
        f"{client_id} added task to queue"
    )

    update_status()

    try:

        client_socket.send(
            f"{client_id} Task received".encode()
        )

    except:
        pass


def handle_worker(worker_socket):

    global worker_id_counter

    worker_id = f"Worker-{worker_id_counter}"

    worker_id_counter += 1

    print(f"{worker_id} Connected")

    workers.append({
        "id": worker_id,
        "socket": worker_socket
    })

    worker_locks.append(
        threading.Lock()
    )

    update_status()


def start_server():

    server = socket.socket()

    server.bind(("localhost", 5000))

    server.listen(5)

    print("Server Running on Port 5000")

    threading.Thread(
        target=queue_worker,
        daemon=True
    ).start()

    while True:

        conn, addr = server.accept()

        try:

            msg = conn.recv(1024).decode()

            if msg == "WORKER":

                threading.Thread(
                    target=handle_worker,
                    args=(conn,),
                    daemon=True
                ).start()

            else:

                threading.Thread(
                    target=handle_client,
                    args=(conn, msg),
                    daemon=True
                ).start()

        except Exception as e:

            print("Connection Error:", e)


if __name__ == "__main__":

    start_server()