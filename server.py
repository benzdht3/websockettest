from email import message
import socket
import select

print("Opening socket...")

server=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR,1)
server.bind(("",6969))
server.listen()
server.setblocking(False)
print("Listening...")
socketlist=[server]
clients={}


def receive_msg(client):
    try:
        msg_header = client.recv(10)
        if not len(msg_header):
            return False
        
        msg_length=int(msg_header.decode("utf-8").strip())
        return {"header": msg_header, "data": client.recv(msg_length)}
    except:
        return False

while True:
    read_socket, _, except_socket = select.select(socketlist, [], socketlist)
    for noti_socket in read_socket:
        if noti_socket == server:
            client_socket, client_addr = server.accept()
            client_socket.setblocking(1)

            user = receive_msg(client_socket)
            if user is False:
                continue

            socketlist.append(client_socket)
            clients[client_socket]=user
            print("New connection from", {client_addr[0]:client_addr[1]}, "username:",user['data'].decode("utf-8"))

        else:
            msg=receive_msg(noti_socket)
            if msg==False:
                print("Close connection from", clients[noti_socket]['data'].decode("utf-8"))
                socketlist.remove(noti_socket)
                del clients[noti_socket]
                continue
            user = clients[noti_socket]
            print("Receive message from", {user['data'].decode("utf-8"): msg['data'].decode("utf-8")})

            for client_socket in clients:
                if client_socket != noti_socket:
                    client_socket.send(user['header']+user['data']+msg['header']+msg['data'])

    for noti_socket in except_socket:
        socketlist.remove[noti_socket]
        del clients[noti_socket]   
server.close()     
    