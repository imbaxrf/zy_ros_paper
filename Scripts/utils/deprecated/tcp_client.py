import socket

client = socket.socket()
client.connect(("127.0.0.1",4444))
while True:
    send_data = input('client>>')
    client.send(send_data.encode('utf-8'))
    if send_data == 'quit':
        break
    recv_data = client.recv(1024).decode('utf-8')
    if recv_data == 'quit':
        break
    print("server>>",recv_data)
client.close()