import socketserver

class ReqHandlerTCP(socketserver.BaseRequestHandler):
    def handle(self):
        print("\033[32mConnected From: %s\033[0m"%str(self.client_address))
        while True:
            data = self.request.recv(1024)
            msg = data.decode('utf-8')
            print("Recv: ", msg)
            if msg == "quit":
                print("\033[31m%s Disconneted.\033[0m"%str(self.client_address))
                break

if __name__ == "__main__":
    addr = ('127.0.0.1', 4444)
    server = socketserver.ThreadingTCPServer(addr, ReqHandlerTCP)
    server.serve_forever() # 永久循环执行