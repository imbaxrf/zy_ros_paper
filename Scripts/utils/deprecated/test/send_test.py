import socket

client = socket.socket()
client.connect(("127.0.0.1",4444))
while True:
    send_data = input('client>>')  #python2.7 raw_input -> python3 input
    client.send(send_data.encode('utf-8'))
    if send_data == "quit":
        break
client.close()

client = socket.socket()
client.connect(("127.0.0.1",5555))
while True:
    send_data = input('client>>')
    client.send(send_data.encode('utf-8'))
    if send_data == "quit":
        break
client.close()