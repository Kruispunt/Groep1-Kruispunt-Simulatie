import socket

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

ip = input('Enter the ip: ')
port = int(input('Enter the port: '))

s.connect((ip, port))

print('Connected')
message = 'Hello, Server!'
s.send(message.encode())
data = s.recv(1024)
print('Received:', data.decode())

s.close()
