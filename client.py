import socket
import time

### CLIENT

print("Client starting")

serverip = "192.168.11.14"
serverport = 11100

try:
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.connect((serverip, serverport))
except ConnectionRefusedError:
    print("The server is not online")
    quit()
print("Client connected")

try:
    def send(data):
        time.sleep(0.5)
        print(">> " + data)
        server.send(str(data).encode())

    def listen():
        found = server.recv(1024).decode()
        print("<< " + found)
        return found

    def reconnect(username):
        if len(username.split(" ")) > 1:
            print("Username must not contain spaces")
            quit()
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.connect((serverip, serverport))
        send("reconnect " + username)
        check = listen()
        if check == "connection accepted":
            print("Connection reconnected")
        elif check == "error not found":
            print("Server error")
            quit()
        else:
            print("error")
            quit()
    def init(username):
        if len(username.split(" ")) > 1:
            print("Username must not contain spaces")
            quit()
        send("newclient")
        check = listen()
        if check == "connection accepted":
            send("username " + username)
        check = listen()
        if check == "username added":
            print("Username ok") # not really necessary

    def requestUsername():
        reconnect(username)
        send("selfuserreq")
        answer = listen()
        if answer == "error not found":
            print("Username not found")
            return
        print("My username is: " + answer + "!")

    def close():
        send("close")

    print("Started up")
    username = input("Enter a username\n--- ")
    print("Checking username...")
    init(username)
    print("# Requesting my username")
    requestUsername()
    close()
except ConnectionResetError:
    print("*** The server was closed ***")
    quit()
except ConnectionAbortedError:
    print("*** The connection was closed ***")
    quit()
