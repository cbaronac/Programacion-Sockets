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
        if not data: 
            print("The server has been finished")  
            # lock released on exit 
            print_lock.release() 
            break
        # reverse the given string from client 
    
  
        # send back reversed string to client 
        
        string_received=data.decode("latin-1")
        bucket_name=string_received.split(" ")
        

        if (bucket_name[0]=="1"):
            name=bucket_name[1]
            createBucket(name,socket_client)
        
        elif (bucket_name[0]=="2"):
            name=bucket_name[1]
            if not os.path.isdir('./Buckets/'+name):
                socket_client.send("The bucket doesn't exists!".encode())
            else:
                deleteBucket(name,socket_client)
            
        elif(bucket_name[0]=="3"):             
            listBuckets(socket_client)

        elif(bucket_name[0]=="4"):
            name=bucket_name[1] #Name of bucket
            nameF=bucket_name[2] #File
            path=bucket_name[3]
            dir="./Buckets/"+name+"/"+nameF   
            f = Path(dir)
            origin=path+"/"+nameF
            if(f.exists()):
                    print("The file alredy exists!")
                    socket_client.send("The file alredy exists!".encode())
            else:
                sizefile = os.path.getsize(origin)
                f= open(dir,"wb")
                uploadFiles(socket_client,f,sizefile)

        elif(bucket_name[0]=="5"):
            bucketName=bucket_name[1]
            if not os.path.isdir('./Buckets/'+bucketName):
                socket_client.send("The bucket doesn't exists!".encode())
            else:
                listFiles(socket_client,bucketName)

        elif(bucket_name[0]=="6"):
            nameBucket=bucket_name[1]
            nameF=bucket_name[2]
            dir="./Buckets/"+nameBucket+"/"+nameF
            deleteFiles(socket_client,dir)

        elif (bucket_name[0]=="7"):
            if not os.path.isdir('./Downloads'):
                os.mkdir("./Downloads")
            nameBucket=bucket_name[1]
            nameFile=bucket_name[2]
            dir="./Downloads/"+nameFile
            f = Path(dir)
            dirOrigin="./Buckets/"+nameBucket+"/"+nameFile
            fOrigin = Path(dirOrigin)
            if(f.exists()):
                print("The file alredy exists!")
            elif not (fOrigin.exists()):
                print("The file doesn't exists!")
            else:
                downloadFiles(nameBucket,nameFile,socket_client)

    
    # connection closed 
    socket_client.send(data) 
    
  
def connectionSocket():
    #Creating a Socket
    socket_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM ) #Socket family type (AF_INET: IPV4), actual type of socket (SOCK_STREAM: TCP)
    print("Socket created...")

    socket_client=socket.socket()

    socket_server.bind((socket.gethostname(),1233))  #Enlazar la tupla IP y Puertos

    socket_server.listen(1)  #Preparing the server for incoming connections and this server will prepare and leave a queue of 5 so it's under some sort
    print("Listening...")
   
    #Accepting a client
    while True:
        socket_client, address = socket_server.accept()  #Address is where they coming from IP address
        print_lock.acquire()
        print('Connected to :', address[0], ':', address[1])
        start_new_thread(threaded, (socket_client,)) 
    
def createBucket(nameBucket,socket_client):
    if not os.path.isdir('./Buckets'):
        os.mkdir("./Buckets")

    dir="./Buckets/"+nameBucket

    try:
        os.mkdir(dir)
        print("The directory has been created successfully.")
        socket_client.send("The bucket has been created successfully!".encode())
    except OSError:
        print("The name of this directory isn't available")
        socket_client.send("The bucket alredy exists!".encode())


def deleteBucket(nameBucket,socket_client):
    dir="./Buckets/"+nameBucket
    try:
        shutil.rmtree(dir) #Borrado en cascada archivos -> Carpeta
    except OSError:
        print("The name of this directory isn't available")
        socket_client.send("The bucket doesn't exists!".encode())
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

def uploadFiles(socket_client,file,sizefile):
    
    while True:
        try:
            # Recibir datos del cliente.
            input_data = socket_client.recv(sizefile)
            if input_data:
                # Compatibilidad con Python 3.
                if isinstance(input_data, bytes):  #Verifica que input_data sean bytes
                    
                    end = input_data[0] == 1
                        
                else:
                    end = input_data == chr(1)  #The chr() function returns the character that represents the specified unicode

                if not end:
                    file.write(input_data)
                    print("The file has been received successfully.")
                    socket_client.send("The file has been received successfully!".encode())
                break

        except:

            print("Error de lectura.")
            file.close()
            break

    file.close() 

def listFiles(socket_client,nameBucket):
    dir="./Buckets/"+nameBucket
    content = os.listdir(dir)
    for i,j in enumerate(content):
        print (i,j)
    print("The files has been listed successfully") 
    socket_client.send("The files has been listed!:".encode())

def deleteFiles(socket_client,dir):
    f = Path(dir)
    if not (f.exists()):
        print("The file doesn't exists!")
        socket_client.send("The file doesn't exists!".encode())
    else:
        remove(dir)
        print("The file has been deleted successfully.") 
        socket_client.send("The file has been deleted from bucket".encode())

def downloadFiles(nameBucket,nameFile,socket_client):
    dir="./Buckets/"+nameBucket+"/"+nameFile
    sizefile = os.path.getsize(dir)
    
    while True:
            
        f = open(dir,"rb")
        content = f.read(sizefile)
            
        while content:
            # Send content
            socket_client.send(content)
            content = f.read(sizefile)
            print("The file has been sent succesfully!")
            socket_client.send("The file has been sent successfully!".encode())
        break

    try:
        socket_client.send(chr(1))
        
    except TypeError:
        
        socket_client.send(bytes(chr(1), "utf-8"))                
                
    f.close()
        


if __name__ == "__main__":
    main()


