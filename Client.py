import socket

def main():
    socketConnection()

def socketConnection():

    #Creating a Socket
    socket_client = socket.socket(socket.AF_INET, socket.SOCK_STREAM ) #Socket family type (AF_INET: IPV4), actual type of socket (SOCK_STREAM: TCP)
    socket_client.connect((socket.gethostname(),1237))
    print('Input commands: ')

    #Sending data
    while True:
        command_to_send=input()
        if (command_to_send=="create"):
            print('Input the bucket name that you want to create: ')
            command_bucket_name=input()
            command_complete=command_to_send+" "+command_bucket_name
            socket_client.send(bytes(command_complete,'utf-8'))
            dataFromServer = socket_client.recv(1024)
            print(dataFromServer)
        elif (command_to_send=="delete"):
            print('Input the bucket name that you want to delete: ')
            command_bucket_name=input()
            command_complete=command_to_send+" "+command_bucket_name
            socket_client.send(bytes(command_complete,'utf-8'))
        elif (command_to_send=="listB"):
            socket_client.send(bytes(command_to_send,'utf-8'))
            
        elif (command_to_send=="listF"):
            print('Input the bucket name that you want to list files : ')
            command_bucket_name=input()
            command_complete=command_to_send+" "+command_bucket_name
            socket_client.send(bytes(command_to_send,'utf-8'))
                
    print("The client has been finished")
    socket_client.close()   

if __name__ == "__main__":
    main()

    '''elif (command_to_send=="upload"):
            print('Input the bucket name that you want to add files: ')
            command_bucket_name=input()
            print('Input the name file: ')
            command_name=input()
            print('Input the type of file: ')
            command_type=input()
            command_complete=command_to_send+" "+command_bucket_name+" "+command_name+" "+command_type
            dir="C:/Users/camil/Desktop/"+command_name+"."+command_type
            f = open(dir,'rb')
            print("Sending...")
            l=f.read(1024)
            while (l):
                print ("Sending...")            
                socket_client.send(l)
                l=f.read(1024)
            print ("Done Sending")
            socket_client.shutdown(socket.SHUT_WR)
            socket_client.close()'''
