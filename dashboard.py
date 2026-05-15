from flask import Flask, render_template, redirect
import subprocess
import json

app = Flask(__name__)

server_process = None

worker_processes = []

client_processes = []


@app.route("/")
def home():

    with open("status.json", "r") as f:

        data = json.load(f)

    return render_template(
        "index.html",
        data=data
    )


@app.route("/start_server")
def start_server():

    global server_process

    if server_process is None:

        server_process = subprocess.Popen(
            ["python", "server.py"]
        )

    return redirect("/")


@app.route("/stop_server")
def stop_server():

    global server_process

    if server_process:

        server_process.terminate()

        server_process = None

    return redirect("/")


@app.route("/add_worker")
def add_worker():

    worker = subprocess.Popen(
        ["python", "worker.py"]
    )

    worker_processes.append(worker)

    return redirect("/")


@app.route("/stop_workers")
def stop_workers():

    global worker_processes

    for worker in worker_processes:

        worker.terminate()

    worker_processes = []

    return redirect("/")


@app.route("/add_client")
def add_client():

    client = subprocess.Popen(
        ["python", "client.py"]
    )

    client_processes.append(client)

    return redirect("/")


@app.route("/stop_clients")
def stop_clients():

    global client_processes

    for client in client_processes:

        client.terminate()

    client_processes = []

    return redirect("/")


if __name__ == "__main__":

    app.run(
        debug=True,
        port=8000
    )