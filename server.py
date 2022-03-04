import socket
import threading


class Server:
    def __init__(self):
        self.ip = socket.gethostbyname(socket.gethostname())
        try:
            self.port = 9090
            self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.s.bind((self.ip, self.port))
        except:
            print("Couldn't bind to that port")

        self.connections = []
        self.accept_connections()

    def accept_connections(self):
        self.s.listen()

        print('Running on IP: ' + self.ip)
        print('Running on port: ' + str(self.port))

        while True:
            c, addr = self.s.accept()
            data = c.recv(1024)
            name_client = data.decode("utf-8")
            print("Connect:", name_client, "\twith adress:", addr)
            c.send(b"Hello, "+data)

            self.connections.append(c)
            print("Connections:", len(self.connections))

            threading.Thread(target=self.handle_client, args=(c, addr,)).start()



    def broadcast(self, sock, data):
        for client in self.connections:
            if client != self.s and client != sock:
                try:
                    client.send(data)
                except:
                    pass


    def handle_client(self, c, addr):
        while 1:
            try:
                data = c.recv(1024)
                try:
                    if data.decode("utf-8") == "disconnect":
                        self.connections.remove(c)
                        print("Disconnect >", addr, "\t Connections now:", len(self.connections))
                        c.close()

                        break
                except:
                    pass
                if len(self.connections) > 1:
                    self.broadcast(c, data)

            except socket.error:
                c.close()


server = Server()