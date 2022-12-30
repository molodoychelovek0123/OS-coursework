import socket


HOST = "localhost"
PORT = 50007


if __name__ == "__main__":
    serverid = 1
    print()
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.connect((HOST, PORT))
        print("Client connected to server " + str(serverid))
        while True:
            # Input
            data = input("Type command (you can use help):")
            if data == "exit":
                print("Close by client")
                break
            if data == "switch":
                if serverid == 1:
                    serverid = 2
                else:
                    serverid = 1
            if data == "help":
                print('Commands: \n    GPU(server 1), screen(server 1), swap(server 2), memory(server 2), close, exit, switch')
            # Send
            else:
                data_bytes = data.encode()
                sock.sendall(data_bytes)
                # Receive
                data_bytes = sock.recv(1024)
                data = data_bytes.decode()
                print("Answer:", data)
                if not data or data == "server closed":
                    print("Closed by server")
                    break
        sock.close()
        print("Client disconnected")
