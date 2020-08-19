import socket
from threading import Thread

client = {}
address = {}

HOST = "127.0.0.1"
PORT = 4444

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((HOST, PORT))


def accept_connections():
    while True:
        conn, addr = s.accept()
        print(f"[#].{addr} Connected")
        conn.send(f"Welcome {addr} to Chart Room".encode())

        address[conn] = addr

        Thread(target=handle_clients, args=(conn, addr)).start()


def broadcast(msg, prefix=""):
    for x in client:
        x.send(bytes(prefix, 'utf8') + msg)


def handle_clients(conn, addr):
    name = conn.recv(1024).decode("utf-8")
    welcome = f"Welcome {name}"
    conn.send(bytes(welcome, 'utf-8'))

    msg = f"{name} has jioned the chatroom."
    broadcast(bytes(msg, 'utf-8'))
    client[conn] = name

    while True:
        msg = conn.recv(1024)

        if msg != bytes("#Quit", "utf-8"):
            broadcast(msg, name + ":")
        else:
            conn.send(bytes("#Quit", ""))
            conn.close()
            del client[conn]
            broadcast(bytes(f"{name} left"))


if __name__ == "__main__":

    s.listen(20)
    print(f"## Server Listening at port {PORT}")

    t1 = Thread(target=accept_connections)

    t1.start()
    t1.join()
