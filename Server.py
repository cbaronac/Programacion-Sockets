#Socket -> Endpoint that receives data, with this one you receive data is not the communication it's the end point that recieves the communicaction on that endpoint sits at an IP and a port
import socket
#import os
import shutil
import pathlib
from os import remove,os

def main():
    connectionSocket()

def connectionSocket():
    #Creating a Socket
    socket_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM ) #Socket family type (AF_INET: IPV4), actual type of socket (SOCK_STREAM: TCP)
    print("Socket created...")

    socket_client=socket.socket()

    socket_server.bind((socket.gethostname(),1237))  #Enlazar la tupla IP y Puertos
    print(f"Socket connected to {socket.gethostname()} by port 1237")
    socket_server.listen(5)  #Preparing the server for incoming connections and this server will prepare and leave a queue of 5 so it's under some sort
    print("Listening...")
    socket_client, address = socket_server.accept()  #Address is where they coming from IP address
    print(f"Connection from {address} has been established!")
    

    #Accepting a client
    while True:
        socket_received=socket_client.recv(1024)
        string_received=socket_received.decode("utf-8")
        bucket_name=string_received.split(" ")
        if (bucket_name[0]=="create"):
            name=bucket_name[1]
            createBucket(name)
            #socket_client.send("The bucket has been created!".encode())
        elif (bucket_name[0]=="delete"):
            name=bucket_name[1]
            deleteBucket(name)
            socket_client.send("The bucket has been deleted!".encode())
        elif(string_received=="listB"):
            name=bucket_name[1]
            name=bucket_name[2]               
            socket_client.send("The buckets has been listed!:".encode())
            listBuckets()
        elif(bucket_name[0]=="upload"):
            name=bucket_name[1] #Name of bucket
            nameF=bucket_name[2] #File
            dir="C:/Users/camil/Desktop/Telemática/Practicas/PracticaSockets/Buckets/"+name+"/"+nameF
            f = open(dir, "wb")
            uploadFiles(nameF,socket_client,f)
        elif(bucket_name[0]=="listF"):
            name=bucket_name[1]
            listFiles(name)
            
        #socket_client.send("The file has been upload into: "+name+" bucket".encode())
        elif (bucket_name[0]=="exit"):
            break

    print("Received:",socket_received.decode("utf-8"))
    print("The server has been finished")
    socket_server.close()

def createBucket(nameBucket):
    dir="C:/Users/camil/Desktop/Telemática/Practicas/PracticaSockets/Buckets/"+nameBucket
    try:
        os.mkdir(dir)
    except OSError:
        print("The name of this directory isn't available")
    else:
        print("The directory has been created")

def deleteBucket(nameBucket):
    dir="C:/Users/camil/Desktop/Telemática/Practicas/PracticaSockets/Buckets/"+nameBucket
    try:
        shutil.rmtree(dir)
    except OSError:
        print("The name of this directory isn't available" % dir)
    else:
        print("The directory has been deleted: %s " % dir)

def listBuckets():
    dir="C:/Users/camil/Desktop/Telemática/Practicas/PracticaSockets/Buckets/"
    content = os.listdir(dir)
    #print(', '.join(content))
    for i,j in enumerate(content):
        print (i,j)

def uploadFiles(nameFile,socket_client,file):
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
                    # Almacenar datos.
                    file.write(input_data)

            print("El archivo se ha recibido correctamente.")     
            break

        except:

            print("Error de lectura.")
            file.close()
            break

    file.close() 

def listFiles(nameBucket):
    dir="C:/Users/camil/Desktop/Telemática/Practicas/PracticaSockets/Buckets/"+nameBucket
    content = pathlib.Path(dir)
    for fichero in content.iterdir():
        print(fichero.name)

def deleteFiles(nameBucket,nameFile):
    remove(nameFile)


if __name__ == "__main__":
    main()


