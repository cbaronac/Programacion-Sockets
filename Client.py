import socket
from pathlib import Path
import os



def main():
    socketConnection()

def menu():
    print('Option |  Name Option', )
    print("  1    |  Create bucket")
    print("  2    |  Delete bucket")
    print("  3    |  List bucket")
    print("  4    |  Upload files")
    print("  5    |  List files")
    print("  6    |  Delete files")
    print("  7    |  Download files")
    print(" ")
    
def socketConnection():

    #Creating a Socket
    socket_client = socket.socket(socket.AF_INET, socket.SOCK_STREAM ) #Socket family type (AF_INET: IPV4), actual type of socket (SOCK_STREAM: TCP)
    socket_client.connect((socket.gethostname(),1237))
    menu()
    print('Input commands: ')
    command_to_send=input()
    menuOptions(command_to_send,socket_client)
    ans = input('\nDo you want to continue(y/n) :') 

    #Sending data
    while True:
        
        while(ans=='y') :
            menu()
            print('Input commands: ')
            command_to_send=input()
            menuOptions(command_to_send,socket_client)
            ans = input('\nDo you want to continue(y/n) :') 
        
        break
    print("The client has been finished")
    socket_client.close()   

def menuOptions(command_to_send,socket_client):

    if (command_to_send=="1"):
        createBucket(command_to_send,socket_client)
    elif (command_to_send=="2"):
        deleteBucket(command_to_send,socket_client)
    elif (command_to_send=="3"):
        listBucket(command_to_send, socket_client)
    elif (command_to_send=="4"):
        upload(command_to_send,socket_client)
    elif (command_to_send=="5"):
        listFiles(command_to_send,socket_client)
    elif (command_to_send=="6"):
        deleteFiles(command_to_send,socket_client)
    elif (command_to_send=="7"):
        downloadFiles(command_to_send,socket_client)
    else:
        print('Input a correct option: ')
        

def createBucket(command_to_send, socket_client):
    print("Input the bucket name that you want to create: ")
    nameBucket=input()
    command_complete=command_to_send+" "+nameBucket
    socket_client.send(bytes(command_complete,'utf-8'))
    confirmationServer(socket_client)

def deleteBucket(command_to_send, socket_client):
    print('Input the bucket name that you want to delete: ')
    command_bucket_name=input()
    command_complete=command_to_send+" "+command_bucket_name
    socket_client.send(bytes(command_complete,'utf-8'))
    confirmationServer(socket_client)

def listBucket(command_to_send, socket_client):
    command_complete=command_to_send
    socket_client.send(bytes(command_to_send,'utf-8'))
    confirmationServer(socket_client)

def upload(command_to_send, socket_client):
    print('Input the bucket name that you want to add files: ')
    command_bucket_name=input()
    print('Input the name file: ')
    command_name=input()
    print('Input the path where is the file:')
    path=input()
    command_complete=command_to_send+" "+command_bucket_name+" "+command_name+" "+path
    socket_client.send(bytes(command_complete,'utf-8'))  
    sizefile = os.path.getsize(path+"/"+command_name)    
    while True:
        dir=path+"/"+command_name
        f = open(dir,"rb")
        content = f.read(sizefile)
        
        while content:
            # Send content
            socket_client.send(content)
            content = f.read(sizefile)
        break

    try:
        socket_client.send(chr(1))
        

    except TypeError:
        
        # Compatibilidad con Python 3.  
        socket_client.send(bytes(chr(1), "utf-8"))                
            
        # Cerrar conexión y archivo.
    f.close()
    print("The file has been sent successfully.")
    confirmationServer(socket_client)

def listFiles(command_to_send, socket_client):
    print('Input the path where are the files that you want to list: ')
    command_bucket_name=input()
    command_complete=command_to_send+" "+command_bucket_name
    socket_client.send(bytes(command_complete,'utf-8'))
    confirmationServer(socket_client)

def deleteFiles(command_to_send,socket_client):
    print('Input the path where is the file that you want to delete: ')
    bucket_name=input()
    print('Input the file name that you want to delete: ')
    command_file_name=input()
    command_complete=command_to_send+" "+bucket_name+" "+command_file_name
    socket_client.send(bytes(command_complete,'utf-8'))
    confirmationServer(socket_client)

def downloadFiles(command_to_send,socket_client):
    print('Input the bucket name where is the file that you want to download: ')
    command_bucket_name=input()
    print('Input the file name that you want to download: ')
    command_file_name=input()
    command_complete=command_to_send+" "+command_bucket_name+" "+command_file_name
    socket_client.send(bytes(command_complete,'utf-8'))
    dir="./Downloads/"+command_file_name
    f = Path(dir)
    if(f.exists()):
        print("The file alredy exists!")
    else:
        downloadIfNotExists(command_bucket_name,command_file_name,socket_client)

def downloadIfNotExists(command_bucket_name,command_file_name, socket_client):
    dire="./Downloads/"+command_file_name
    file= open(dire,"wb")
    dir="./Buckets/"+command_bucket_name+"/"+command_file_name
    sizefile = os.path.getsize(dir)
    while True:
        try:
            # Recibir datos del cliente.
            input_data = socket_client.recv(sizefile)
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
                        confirmationServer()                
            break

        except:
           
            file.close()
            break

    file.close() 


def confirmationServer(socket_client):
    dataFromServer = socket_client.recv(1024)
    print(dataFromServer)


if __name__ == "__main__":
    main()

 