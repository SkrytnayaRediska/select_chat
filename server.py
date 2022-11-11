import select
from socket import socket, AF_INET, SOCK_STREAM


def client_read(r_clients, client_list):
    responses = dict()
    for sock in r_clients:
        try:
            data = sock.recv(1024).decode('utf-8')
            responses[sock] = data
            print(f"Client {sock.getpeername()} says: {data}")
        except:
            print("Client closed")
            client_list.remove(sock)

    return responses


def client_write(requests, w_clients, all_clients):
    for sock in w_clients:
        if sock in requests:
            try:
                response = requests[sock].encode('utf-8')
                sock.sendall(response.upper())
            except:
                print(f"Client {sock.fileno()} {sock.getpeername()} closed")
                sock.close()
                all_clients.remove(sock)


def main_server():
    address = ('localhost', 3333)
    clients = list()

    sock = socket(AF_INET, SOCK_STREAM)
    sock.bind(address)
    sock.listen(5)
    sock.settimeout(0.2)
    while True:
        try:
            conn, addr = sock.accept()
        except OSError as e:
            pass      # timeout!
        else:
            print(f"Got a connection request from {addr}")
            clients.append(conn)
        finally:
            wait = 10
            r = list()
            w = list()
            try:
                r, w, e = select.select(clients, clients, [], wait)
            except:
                pass
            requests = client_read(r, clients)
            if requests:
                client_write(requests, w, clients)


print("SERVER IS RUNNING")

main_server()
