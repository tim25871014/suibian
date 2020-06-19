import socket

HOST = '210.71.78.200'
HOST = '127.0.0.1'
PORT = 8000
clientMessage = input()

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((HOST, PORT))
client.sendall(clientMessage.encode())

serverMessage = str(client.recv(1024), encoding='utf-8')
print('Server:', serverMessage)

client.close()
