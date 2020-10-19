#Socket -> Endpoint that receives data, with this one you receive data is not the communication it's the end point that recieves the communicaction on that endpoint sits at an IP and a port
import socket


#Conection without socket.close()
#We use a header to notify your program how long is your message and other informations
#HEADERSIZE = 10

#Creating a Socket
socket_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM ) #Socket family type (AF_INET: IPV4), actual type of socket (SOCK_STREAM: TCP)
print("Socket created...")

socket_client=socket.socket()

socket_server.bind((socket.gethostname(),1237))  #Enlazar la tupla IP y Puertos
print(f"Socket connected to {socket.gethostname()} by port 1237")
socket_server.listen(5)  #Preparing the server for incoming connections and this server will prepare and leave a queue of 5 so it's under some sort
print("Listening...")


#Accepting a client
socket_client, address = socket_server.accept()
print(f"Connection from {address} has been established!")

while True:
    socket_received=socket_client.recv(1024)

    if socket_received.decode("utf-8")=="salir":
        break
    print("Received:",socket_received.decode("utf-8"))

print("The server has been finished")
socket_server.close()

'''
while True:
    clientsocket, address = s.accept()  #Address is where they coming from IP address
    print(f"Connection from {address} has been established!")
    
    d={1:"Hey",2:"There"}
    msg=pickle.dumps(d)
    
    msg=bytes(f'{len(msg):<{HEADERSIZE}}',"utf-8")+msg

    clientsocket.send(msg) #Send information to the client socker (Message, type of bytes)
'''


