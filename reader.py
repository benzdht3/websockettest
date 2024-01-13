import socket
import select
import errno
import sys

myusername = "Reader"

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(("locahost",1234))
client.setblocking(False)

username=myusername.encode("utf-8")
username_header =f"{len(username):<{10}}".encode("utf-8")
client.send(username_header+username)
while True:
    msg = ""
    if msg:
        msg=msg.encode("utf-8")
        msg_header=f"{len(msg):<{10}}".encode("utf-8")
        client.send(msg_header+msg)
    try:
        while True:
            username_header=client.recv(10)
            if not len(username_header):
                print("Server closed")
                sys.exit()
            username_length=int(username_header.decode("utf-8").strip())
            username=client.recv(username_length).decode("utf-8")
            
            msg_header=client.recv(10)
            msg_length=int(msg_header.decode("utf-8").strip())
            msg=client.recv(msg_length).decode("utf-8")

            print(username,">",msg)
    except IOError as e:
        if e.errno != errno.EAGAIN and e.errno != errno.EWOULDBLOCK:
            print('Reading error',str(e))
            sys.exit()
        continue
    
    except Exception as e:
        print('General error',str(e))
        sys.exit()