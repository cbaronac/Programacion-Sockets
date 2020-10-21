#Socket -> Endpoint that receives data, with this one you receive data is not the communication it's the end point that recieves the communicaction on that endpoint sits at an IP and a port
import socket
import os
import shutil
import pathlib
from os import remove
from pathlib import Path
from _thread import *
import threading 

print_lock = threading.Lock() 
  

def main():
    connectionSocket()

def threaded(socket_client):
    while True: 
        # data received from client 
        data = socket_client.recv(1024) 
        print(data)
        if not data: 
            print("The server has been finished")  
            # lock released on exit 
            print_lock.release() 
            break
        # reverse the given string from client 
    
  
        # send back reversed string to client 
        
        string_received=data.decode("utf-8")
        bucket_name=string_received.split(" ")
        

        if (bucket_name[0]=="1"):
            name=bucket_name[1]
            createBucket(name,socket_client)

        elif (bucket_name[0]=="2"):
            name=bucket_name[1]
            deleteBucket(name,socket_client)
            
        elif(bucket_name[0]=="3"):             
            listBuckets(socket_client)

        elif(bucket_name[0]=="4"):
            name=bucket_name[1] #Name of bucket
            nameF=bucket_name[2] #File
            dir="./Buckets/"+name+"/"+nameF
            f= open(dir,"wb")
            uploadFiles(nameF,socket_client,f,dir)

        elif(bucket_name[0]=="5"):
            dir=bucket_name[2]
            listFiles(socket_client,dir)

        elif(bucket_name[0]=="6"):
            path=bucket_name[1]
            nameF=bucket_name[2]
            dir=path+"/"+nameF
            deleteFiles(socket_client,dir)

        elif (bucket_name[0]=="7"):
            nameBucket=bucket_name[1]
            nameFile=bucket_name[2]

            downloadFiles(nameBucket,nameFile,socket_client)
        #socket_client.send("The file has been upload into: "+name+" bucket".encode())
    
    # connection closed 
    socket_client.send(data) 
    
  
def connectionSocket():
    #Creating a Socket
    socket_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM ) #Socket family type (AF_INET: IPV4), actual type of socket (SOCK_STREAM: TCP)
    print("Socket created...")

    socket_client=socket.socket()

    socket_server.bind((socket.gethostname(),1237))  #Enlazar la tupla IP y Puertos

    socket_server.listen(5)  #Preparing the server for incoming connections and this server will prepare and leave a queue of 5 so it's under some sort
    print("Listening...")
   
    #Accepting a client
    while True:
        socket_client, address = socket_server.accept()  #Address is where they coming from IP address
        print(f"Connection from {address} has been established!")
        print_lock.acquire()
        print('Connected to :', address[0], ':', address[1])
        start_new_thread(threaded, (socket_client,)) 
    
def createBucket(nameBucket,socket_client):
    if not os.path.isdir('./Buckets'):
        os.mkdir("./Buckets")

    dir="./Buckets/"+nameBucket
    try:
        os.mkdir(dir)
    except OSError:
        print("The name of this directory isn't available")
    else:
        print("The directory has been created successfully.")
    socket_client.send("The bucket has been created!".encode())

def deleteBucket(nameBucket,socket_client):
    dir="./Buckets/"+nameBucket
    try:
        shutil.rmtree(dir)
    except OSError:
        print("The name of this directory isn't available")
    else:
        print("The directory has been deleted successfully.")
    socket_client.send("The bucket has been deleted!".encode())

def listBuckets(socket_client):
    dir="./Buckets"
    content = os.listdir(dir)
    for i,j in enumerate(content):
        print (i,j)
    print("The buckets has been listed on server successfully.") 
    socket_client.send("The buckets has been listed!:".encode())

def uploadFiles(nameFile,socket_client,file,dire):
    while True:
        try:
            # Recibir datos del cliente.
            input_data = socket_client.recv(1024)
            print(input_data)
            if input_data:
                # Compatibilidad con Python 3.
                if isinstance(input_data, bytes):
                    end = input_data[0] == 1
                    
                else:
                    end = input_data == chr(1)
                   
                if not end:
                    if os.path.isdir(dire):
                        print("The file exists!")
                    else:
                        file.write(input_data)
                        print("The file has been received successfully.")
            break

        except:

            print("Error de lectura.")
            file.close()
            break

    file.close() 

def listFiles(socket_client,dir):
    content = pathlib.Path(dir)
    for fichero in content.iterdir():
        print(fichero.name)
    print("The files has been listed successfully") 
    socket_client.send("The files has been listed!:".encode())

def deleteFiles(socket_client,dir):
    remove(dir)
    print("The file has been deleted successfully.") 
    socket_client.send("The file has been deleted from bucket".encode())

def downloadFiles(nameBucket,nameFile,socket_client):
    if not os.path.isdir('./Downloads'):
        os.mkdir("./Downloads")
    
    while True:
        dir="./Buckets/"+nameBucket+"/"+nameFile
        f = open(dir,"rb")
        content = f.read(1024)
        
        while content:
            # Send content
            socket_client.send(content)
            content = f.read(1024)
        break

    try:
        socket_client.send(chr(1))
        print(socket_client.send(chr(1)))

    except TypeError:
        
        # Compatibilidad con Python 3.  
        socket_client.send(bytes(chr(1), "utf-8"))                
            
        # Cerrar conexión y archivo.
    f.close()
    print("The file has been sent successfully.")
  


if __name__ == "__main__":
    main()


