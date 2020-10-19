import socket

#HEADERSIZE = 10

socket_client = socket.socket(socket.AF_INET, socket.SOCK_STREAM ) #Socket family type (AF_INET: IPV4), actual type of socket (SOCK_STREAM: TCP)
socket_client.connect((socket.gethostname(),1237))
print('Input commands: ')

while True:
    command_to_send=input()
    socket_client.send(bytes(command_to_send,'utf-8'))

    if (command_to_send=="salir"):
        break

print("The client has been finished")
socket_client.close()


'''
def main():
    print('Input commands: ')
    command_to_send=input()

    while command_to_send!='QUIT':
        if (command_to_send=='DATA'):
            data_to_send=input('Input data to send: ')
            command_and_data_to_send = command_to_send + ' ' + data_to_send
            s.send(bytes(command_and_data_to_send).encode())
            s.recv(16)
            print('Data')
            
        else:
            print('Nada')

    if __name__ == "__main__":
        main()

    

        

        full_msg = b''
        new_msg=True
        while True:
            msg = s.recv(16) #Recieve a chunks of data with a size of 1024 bytes
            if new_msg:
                print(f"new message length: {msg[:HEADERSIZE]}")
                msglen=int(msg[:HEADERSIZE])
                new_msg=False

            full_msg+= msg

            if len(full_msg)-HEADERSIZE == msglen:
                print("full msg recvd")
                print(full_msg[HEADERSIZE:])
                
                d=pickle.loads(full_msg[HEADERSIZE:])
                print(d)

                new_msg=True
                full_msg=b''

        print(full_msg)
        '''
