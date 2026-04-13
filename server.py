import socket
import threading

workers = []
worker_index = 0
def handle_client(client_socket, first_message):
    global worker_index

    try:
        data = first_message
        print("Client task:", data)

        if not workers:
            client_socket.send("No worker available".encode())
            return

        worker = workers[worker_index % len(workers)]
        worker_index += 1

        worker.send(data.encode())
        result = worker.recv(1024).decode()

        print("Result:", result)

        # LOGGING
        with open("log.txt", "a") as f:
            f.write(f"Task: {data} | Result: {result}\n")

        client_socket.send(result.encode())

    except Exception as e:
        print("Error:", e)

    finally:
        client_socket.close()

def handle_worker(worker_socket):
    print("Worker connected")
    workers.append(worker_socket)


def start_server():
    server = socket.socket()
    server.bind(("localhost", 5000))
    server.listen(5)

    print("Server running on port 5000...")

    while True:
        conn, addr = server.accept()

        try:
            msg = conn.recv(1024).decode()

            if msg == "WORKER":
                threading.Thread(target=handle_worker, args=(conn,), daemon=True).start()
            else:
                threading.Thread(target=handle_client, args=(conn, msg), daemon=True).start()

        except Exception as e:
            print("Connection error:", e)


start_server()
