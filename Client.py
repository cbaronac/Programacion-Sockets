import socket
from pathlib import Path
import os

def main():
    ''' 
        Main method of the application 
    '''

    socketConnection()

def menu():

    '''
        Main menu of the application 
        This method shows the possible commands and options that a client can run
    '''

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

    '''
        This method establish the connection of the client with Sockets 
    '''

    #Creating a Socket
    socket_client = socket.socket(socket.AF_INET, socket.SOCK_STREAM ) #Socket family type (AF_INET: IPV4), actual type of socket (SOCK_STREAM: TCP)
    socket_client.connect((socket.gethostname(),1233))
    initialMenu(socket_client)

def initialMenu(socket_client):
    ''' 
        This method is responsible for asking the client the menu commands that he want to execute and closing the connection with the socket
    '''
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
    '''
        This method verifies the main command that the client chooses in the menu and calls the methods responsible for doing the chosen action.
    '''
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
    ''' 
        This method create a Bucket, for this is necesary input a bucket name

        If the bucket name is empty, The client will continue to be notified that they must enter a valid name

        If the bucket is created successfully, the client will be notified with a message sent from the server
    '''

    print("Input the bucket name that you want to create: ")
    bucket_name=input()
    while(bucket_name=="" or bucket_name==" "):
        print("Input a correct bucket name: ")
        bucket_name=input()
    command_complete=command_to_send+" "+bucket_name
    socket_client.send(bytes(command_complete,'utf-8'))
    confirmationServer(socket_client)

def deleteBucket(command_to_send, socket_client):

    ''' 
        This method detele a Bucket, for this is necesary input a bucket name that you want to delete

        If the bucket name is empty, The client will continue to be notified that they must enter a valid name

        If the bucket is delete successfully, the client will be notified with a message sent from the server
    '''
    print('Input the bucket name that you want to delete: ')
    bucket_name=input()
    while(bucket_name=="" or bucket_name==" "):
        print("Input a correct bucket name: ")
        bucket_name=input()
    command_complete=command_to_send+" "+bucket_name
    socket_client.send(bytes(command_complete,'utf-8'))
    confirmationServer(socket_client)

def listBucket(command_to_send, socket_client):
    ''' 
        This method lists the Buckets

        If the buckets are listed successfully, the client will be notified with a message sent from the server
    '''
    socket_client.send(bytes(command_to_send,'utf-8'))
    confirmationServer(socket_client)

def upload(command_to_send, socket_client):
    ''' 
        This method allows uploading a file saved in any client path to a specific bucket, for this is necesary input the bucket name, 
        file name with its corresponding extension (Ex: .png .jpg .txt) and also the path where is saved this file

        If the bucket name, file name or path are empty, or the bucket doesn't exists, he client will continue to be notified that they must enter a valid command, 
        
        If the file is if the file is uploaded correctly, the client will be notified with a message sent from the server

        The function of this method is read a file stored in a client's machine, for that we need to recieved the size of the file in bytes
        and then send it to the server
    '''

    print('Input the bucket name that you want to add files: ')
    bucket_name=input()
    while(bucket_name=="" or bucket_name==" " or not os.path.isdir('./Buckets/'+bucket_name)):
        print("Input a correct bucket name: ")
        bucket_name=input()

    print('Input the name file with the extension type (Ex: fileName.png): ')
    file_name=input()
    while(file_name=="" or file_name==" " ):
        print("Input a correct file name: ")
        file_name=input()
    print('Input the path where is the file:')
    path=input()
    while(path=="" or path==" "):
        print("Input a correct path: ")
        path=input()
    origin=path+"/"+file_name
    fOrigin=Path(origin)
    if (fOrigin.exists()):
        command_complete=command_to_send+" "+bucket_name+" "+file_name+" "+path
        socket_client.send(bytes(command_complete,'utf-8'))  
        sizefile = os.path.getsize(path+"/"+file_name)    
        while True:
            dir=path+"/"+file_name
            f = open(dir,"rb")
            content = f.read(sizefile)
                
            while content:
                
                socket_client.send(content)
                content = f.read(sizefile)
            break

        try:
            socket_client.send(chr(1))        
        except TypeError:
            socket_client.send(bytes(chr(1), "utf-8"))                           
        
        f.close()
        print("The file has been sent successfully.")
        confirmationServer(socket_client)
    else:
         print("The file doesn't exists!")


def listFiles(command_to_send, socket_client):
    ''' 
        This method lists the files that are stored in a specific bucket, for this is necesary input the bucket name

        If the bucket name is empty, The client will continue to be notified that they must enter a valid name

        If the bucket's files are listed successfully, the client will be notified with a message sent from the server
    '''
    print('Input the bucket name where are the files that you want to list: ')
    bucket_name=input()
    while(bucket_name=="" or bucket_name==" "):
        print("Input a correct bucket name: ")
        bucket_name=input()
    command_complete=command_to_send+" "+bucket_name
    socket_client.send(bytes(command_complete,'utf-8'))
    confirmationServer(socket_client)

def deleteFiles(command_to_send,socket_client):

    ''' 
        This method detele Bucket's files, for this is necesary input the bucket and file name 

        If the bucket name and file name are empty, or the bucket doesn't exists the client will continue to be notified that they must enter a valid name

        If bucket's file is delete successfully, the client will be notified with a message sent from the server
    '''
    print('Input the bucket name where is the file that you want to delete: ')
    bucket_name=input()
    while(bucket_name=="" or bucket_name==" " or not os.path.isdir('./Buckets/'+bucket_name)):
        print("Input a correct bucket name: ")
        bucket_name=input()
    print('Input the file name that you want to delete with the extension type (Ex: fileName.png): ')
    file_name=input()
    while(file_name=="" or file_name==" "):
        print("Input a correct file name with the extension type (Ex: fileName.png): ")
        file_name=input()
    command_complete=command_to_send+" "+bucket_name+" "+file_name
    socket_client.send(bytes(command_complete,'utf-8'))
    confirmationServer(socket_client)

def downloadFiles(command_to_send,socket_client):
    ''' 
        This method allows downloading a file saved stored in server's bucket in a client's binder call downloads
        for this is necesary input the bucket name, file name with its corresponding extension (Ex: .png .jpg .txt) 

        If the bucket name or file name are empty, or the bucket doesn't exists, the client will continue to be notified that they must enter a valid command, 
            
        If the file alredy exists in client downloads or doesn't exists in the bucket, the server will notified 
    '''

    print('Input the bucket name where is the file that you want to download: ')
    bucket_name=input()
    while(bucket_name=="" or bucket_name==" " or not os.path.isdir('./Buckets/'+bucket_name)):
        print("Input a correct bucket name: ")
        bucket_name=input()
    print('Input the file name that you want to download with the extension type (Ex: fileName.png): ')
    file_name=input()
    while(file_name=="" or file_name==" "):
        print("Input a correct name file with the extension type (Ex: fileName.png): ")
        file_name=input()
    command_complete=command_to_send+" "+bucket_name+" "+file_name
    socket_client.send(bytes(command_complete,'utf-8'))
    dir="./Downloads/"+file_name
    f = Path(dir)
    dirOrigin="./Buckets/"+bucket_name+"/"+file_name
    fOrigin = Path(dirOrigin)
    if(f.exists()):
        print("The file alredy exists!")
    elif not (fOrigin.exists()):
        print("The file doesn't exists!")
    else:
        downloadIfNotExists(file_name,socket_client,dirOrigin)

def downloadIfNotExists(file_name, socket_client,dirOrigin):

    ''' 
        This method runs when a file doesn't exists in client's binder and when the file exists in a specific bucket

        The function of this method is write in client's binder called downloads a file stored in a specific bucket, for that we
        need to recieved the size of the file in bytes

        If the file is downloaded correctly, the client will be notified with a message sent from the server
    '''

    dire="./Downloads/"+file_name
    file= open(dire,"wb")
    sizefile = os.path.getsize(dirOrigin)
    while True:
        try:
            input_data = socket_client.recv(sizefile)

            if input_data:
                
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
                        confirmationServer(socket_client)                
            break

        except:
            file.close()
            break

    file.close() 



def confirmationServer(socket_client):
    '''
        This method has the function of receiving the message sent by the server and displaying it on the client
    '''
    dataFromServer = socket_client.recv(1024)
    string_received=dataFromServer.decode("utf-8")
    print(string_received)


if __name__ == "__main__":

    '''
        Call of the main method of the application
    '''

    main()

 