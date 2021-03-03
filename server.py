import socket

### SERVER

"""

TODO: implement an option to choose ip and port on the client side
FIXME: on client reconnect and data transfer, no data is received.

"""
print("Server starting")

serverip = "192.168.11.14"
serverport = 11100

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((serverip, serverport))
server.listen(10)

print("Server connected")
clients = []

def searchClients(client):
    i = 0
    for c in clients:
        if c[0] == client:
            print("Old client found")
            print("Client index " + str(i))
            return i
        i = i + 1
    print("New client found")
    return -1

def searchUsernames(name):
    i = 0
    for c in clients:
        if c[1] == name:
            print("Username found, index " + str(i))
            return i
        i = i + 1
    print("Username not found")
    return -1

def send(message, client):
    print(">> " + message)
    client.send(str(message).encode())

def handle(data, client, address):
    if data == "newclient":
        if searchClients(client) == -1:
            clients.append([client, address])
        send("connection accepted", client)
        data = client.recv(1024).decode()
        username = data.split(" ")[1]
        clients[-1].append(username)
        send("username added", client)
    elif data.split(" ")[0] == "reconnect":
        oldusername = data.split(" ")[1]
        userid = searchUsernames(oldusername)
        if userid == -1:
            send("error not found", client)
            return
        clients[userid][0] = client
        send("connection accepted", client)
    elif data.split(" ")[0] == "selfuserreq":
        clientid = searchClients(client)
        if clientid == -1:
            send("error not found", client)
            return
        send(clients[clientid][2], client)
    elif data == "close":
        clientid = searchClients(client)
        clients.remove(clientid)
        print("Client removed")


while True:
    print("+ CONNECTIONS ALLOWED +                             *")
    try:
        client, address = server.accept()
        print("NEW CONNECTION")
        data = client.recv(1024).decode()
        if len(data) > 0:
            print("<< " + data)
            handle(data, client, address)
        else:
            print("!! EMPTY DATA")
        client.close()
    except ConnectionResetError:
        print("!! CLIENT DISCONNECTED")
        client.close()
    print("CONNECTION CLOSED")
