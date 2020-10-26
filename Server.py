# Code by:
# Camila Barona and Camila Mejia

import socket
import os
import shutil
from os import remove
from pathlib import Path
from _thread import *
import threading 

print_lock = threading.Lock() 
  

def main():
    ''' 
        Main method of the application 
    '''
    connectionSocket()

def threaded(socket_client):
    ''' 
        This method is responsible for implementing the operation of threads in order to allow connecting several clients to the server 
        also receives the command sent by the client and calls the corresponding method depending on the function that the client wants to do
    '''

    while True: 
        # data received from client 
        data = socket_client.recv(1024) 
        if not data: 
            print("The server has been finished") 
            # lock released on exit 
            print_lock.release() 
            break
        

        string_received=data.decode("latin-1")
        command_from_client=string_received.split(" ")
        

        if (command_from_client[0]=="1"):
            bucket_name=command_from_client[1]
            createBucket(bucket_name,socket_client)
        
        elif (command_from_client[0]=="2"):
            bucket_name=command_from_client[1]
            if not os.path.isdir('./Buckets/'+bucket_name):
                socket_client.send("The bucket doesn't exists!".encode())
            else:
                deleteBucket(bucket_name,socket_client)
            
        elif(command_from_client[0]=="3"):             
            listBuckets(socket_client)

        elif(command_from_client[0]=="4"):
            bucket_name=command_from_client[1] 
            file_name=command_from_client[2] 
            path=command_from_client[3]
            dir="./Buckets/"+bucket_name+"/"+file_name   
            f = Path(dir)
            origin=path+"/"+file_name
            if(f.exists()):
                    print("The file alredy exists!")
                    socket_client.send("The file alredy exists!".encode())
            else:
                sizefile = os.path.getsize(origin)
                f= open(dir,"wb")
                uploadFiles(socket_client,f,sizefile)

        elif(command_from_client[0]=="5"):
            bucket_name=command_from_client[1]
            if not os.path.isdir('./Buckets/'+bucket_name):
                socket_client.send("The bucket doesn't exists!".encode())
            else:
                listFiles(socket_client,bucket_name)

        elif(command_from_client[0]=="6"):
            bucket_name=command_from_client[1]
            file_name=command_from_client[2]
            dir="./Buckets/"+bucket_name+"/"+file_name
            deleteFiles(socket_client,dir)

        elif (command_from_client[0]=="7"):
            if not os.path.isdir('./Downloads'):
                os.mkdir("./Downloads")
            bucket_name=command_from_client[1]
            file_name=command_from_client[2]
            dir="./Downloads/"+file_name
            f = Path(dir)
            dirOrigin="./Buckets/"+bucket_name+"/"+file_name
            fOrigin = Path(dirOrigin)
            if(f.exists()):
                print("The file alredy exists!")
            elif not (fOrigin.exists()):
                print("The file doesn't exists!")
            else:
                downloadFiles(bucket_name,file_name,socket_client)

    
    # connection closed 
    socket_client.send(data)
    
    
  
def connectionSocket():
    '''
        This method establish the connection of the client with Sockets 
    '''

    #Creating a Socket
    socket_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM ) #Socket family type (AF_INET: IPV4), actual type of socket (SOCK_STREAM: TCP)
    print("Socket created...")

    socket_client=socket.socket()

    socket_server.bind((socket.gethostname(),1233)) #Bind the IP tuple and Ports

    socket_server.listen(5) 
    print("Listening...")
    #it specifies the number of unaccepted connections that the system will allow before refusing new connections. 
    # If not specified, a default reasonable value is chosen.
   
    #Accepting a client
    while True:
        socket_client, address = socket_server.accept()  #Address is where they coming from IP address
        print_lock.acquire()
        print('Connected to :', address[0], ':', address[1])
        start_new_thread(threaded, (socket_client,)) 
    
def createBucket(bucket_name,socket_client):
    ''' 
        This method create a Bucket, for this is necesary input a bucket name

        The main binder where the buckets will be stored will be created in the path where the application is run

        If the bucket is created successfully, the client will be notified with a message sent from the server

        The buckets are created using os library
    '''

    if not os.path.isdir('./Buckets'):
        os.mkdir("./Buckets")

    dir="./Buckets/"+bucket_name

    try:
        os.mkdir(dir)
        print("The directory has been created successfully.")
        socket_client.send("The bucket has been created successfully!".encode())
    except OSError:
        print("The name of this directory isn't available")
        socket_client.send("The bucket alredy exists!".encode())


def deleteBucket(bucket_name,socket_client):
    ''' 
        This method delete a Bucket, for this is necesary input a bucket name

        The main binder where the buckets will be stored will be created in the path where the application is run

        If the bucket is deleted successfully, the client will be notified with a message sent from the server

        The buckets are deleted using shutil library
    '''

    dir="./Buckets/"+bucket_name
    try:
        shutil.rmtree(dir) #Cascading Delete Files -> Folder
        print("The directory has been deleted successfully.")
        socket_client.send("The bucket has been deleted!".encode())
    except OSError:
        print("The name of this directory isn't available")
        socket_client.send("The bucket doesn't exists!".encode())

def listBuckets(socket_client):
    ''' 
        This method lists the Buckets

        If the buckets are listed successfully, the client will be notified with a message sent from the server

        The buckets are listed using os library
    '''

    dir="./Buckets"
    list_buckets=""
    content = os.listdir(dir)
    for i,j in enumerate(content):
        list_buckets= list_buckets + str(i+1) +"->"+str(j) + "\n"
        print (i,j)
    socket_client.send(list_buckets.encode())
    print("The buckets has been listed on server successfully.")     

def uploadFiles(socket_client,file,sizefile):
    ''' 
        This method allows uploading a file stored in server's bucket in a client's binder call downloads
        
        The function of this method is write in a bucket a file stored in specific path, for that we need to recieved the size of the file in bytes

        If the file is uploading correctly, the client will be notified with a message sent from the server
    '''
    while True:
        try:
            
            input_data = socket_client.recv(sizefile)
            if input_data:
                
                if isinstance(input_data, bytes):  #Verify that input_data are bytes

                    end = input_data[0] == 1

                else:
                    end = input_data == chr(1)  #End checks if it is in the header or end of the file if it is false stop writing

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

    ''' 
        This method lists the files that are stored in a specific bucket, for this is necesary input the bucket name

        The bucket's files are listed using os library
    '''

    dir="./Buckets/"+nameBucket
    list_files=""
    content = os.listdir(dir)
    for i,j in enumerate(content):
        list_files= list_files + str(i+1) +"->"+str(j) + "\n"
        print (i,j)
    print("The files has been listed successfully") 
    socket_client.send(list_files.encode())


def deleteFiles(socket_client,dir):

    ''' 
        This method delete a file stores in a Bucket

        If bucket's file is deleted successfully, the client will be notified with a message sent from the server
    '''

    f = Path(dir)
    if not (f.exists()):
        print("The file doesn't exists!")
        socket_client.send("The file doesn't exists!".encode())
    else:
        remove(dir)
        print("The file has been deleted successfully.") 
        socket_client.send("The file has been deleted from bucket".encode())

def downloadFiles(bucket_name,file_name,socket_client):
    
    ''' 
        This method allows downloading a file saved stored in server's bucket in a client's binder call downloads 

        The function of this method is read a file stored in a bucket, for that we need to send the size of the file in bytes

        If the file is downloading correctly, the client will be notified with a message sent from the server
    '''

    dir="./Buckets/"+bucket_name+"/"+file_name
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


