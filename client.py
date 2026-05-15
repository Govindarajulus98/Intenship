import socket
import json


def send_task(task):

    try:

        client = socket.socket()

        client.connect(("localhost", 5000))

        print("Sending Task:", task)

        client.send(json.dumps(task).encode())

        response = client.recv(1024).decode()

        print("Server:", response)

        try:

            result = client.recv(1024).decode()

            if result:
                print("Result:", result)

        except:
            pass

        print("----------------------")

        client.close()

    except Exception as e:

        print("Client Error:", e)


def run_client():

    try:

        with open("tasks.txt", "r") as f:

            for line in f:

                line = line.strip()

                if not line:
                    continue

                try:

                    task = json.loads(line)

                    send_task(task)

                except json.JSONDecodeError:

                    print("Invalid JSON:", line)

    except FileNotFoundError:

        print("tasks.txt not found")


if __name__ == "__main__":

    run_client()