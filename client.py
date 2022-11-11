import socket
import sys

PLACE = ('localhost', 3333)

def client():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect(PLACE)
    while True:
        message = input("Enter a message: ")
        sock.send(message.encode('utf-8'))
        receive = sock.recv(1024).decode('utf-8')
        print("Responce:", receive)

client()