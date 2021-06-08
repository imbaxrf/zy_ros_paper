import socket


class ServerUDP: 
    def __init__(self,ip = "127.0.0.1",port = 4444):
        self.ip = ip
        self.port = port
        self._server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self._server.bind((ip,port))
        self._server.settimeout(10)
        print("Server Started.")
    def __del__(self):
        print("Server Closed.")
        self._server.close()
    def recv_msg(self):
        try:
            recv_data,address = self._server.recvfrom(1024)
            recv_data = recv_data.decode('utf-8')
            return recv_data
        except socket.timeout:
            return "Time out!"
    def send_msg(self,msg:str):
        self._server.sendto(msg.encode('utf-8'),(self.ip,self.port))

class ClientUDP: 
    def __init__(self,ip = "127.0.0.1",port = 4444):
        self.ip = ip
        self.port = port
        self._client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        #self._client.bind((ip,port))
        #self._client.settimeout(10)
        print("Client Started.")
    def __del__(self):
        print("Client Closed.")
        self._client.close()
    def recv_msg(self):
        try:
            recv_data,address = self._client.recvfrom(1024)
            recv_data = recv_data.decode('utf-8')
            return recv_data
        except socket.timeout:
            return "Time out!"
    def send_msg(self,msg:str):
        self._client.sendto(msg.encode('utf-8'),(self.ip,self.port))



