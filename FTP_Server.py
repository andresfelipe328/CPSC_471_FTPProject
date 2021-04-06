# =====================================================================================================================
#
# =====================================================================================================================

# Imports
import socket
import sys
import os

#Global Variable
FORMAT = "utf-8"


# == TransjerData =====================================================================================================

def TransferData(userFile, client):
    # Open file and read bytes
    with open(userFile, 'r') as File:
        # Start reading file
        bytesSend = File.read(1024)
        
        # Send what's being read to Client
        client.send(bytesSend.encode(FORMAT))
        
        # If file content exceeds 1024 bytes
        while bytesSend != "":
            bytesSend = File.read(1024)
            client.send(bytesSend)







# == DoesExist ========================================================================================================

def DoesExist(userFile, client):
    if (os.path.isfile(userFile)):
        userFileSize = str(os.path.getsize(userFile))
        client.send(userFileSize.encode(FORMAT))
        print("    A file of [" + str(userFileSize) + "]bytes was sent to client")
        return True
    return False





# == Server ===========================================================================================================

def Server():
    # Variables
    SERV_PORT = int(sys.argv[1])                                        # Port number
    SERVER = socket.gethostbyname(socket.gethostname())                 # Server's IP address
    SERV_SOCKET = socket.socket(socket.AF_INET, socket.SOCK_STREAM)     # Server's Socket
    SERV_SOCKET.bind((SERVER, SERV_PORT))                               # Bind the Server with Port Number
    QUIT = "quit"                                                       # input to end connection

    # Pepare for possible connections
    SERV_SOCKET.listen(1)
    print("Server [" + str(SERVER) + "] is searching for connections")

    # Let client connect
    while True:
        # Gets Info from the client
        conn, address = SERV_SOCKET.accept()
        print(" Client with IP address [" + str(address) + "] is connected")
        
        # Server receives data from Client
        clientData = conn.recv(1024).decode(FORMAT)

        # If client does not send quit, download, upload, or ls
        if (clientData != QUIT):
            if not DoesExist(clientData, conn):
                print("File does not exist")
            else:
                # if client wants to continue, send content of file
                confirmation = conn.recv(1024).decode(FORMAT)
                if (confirmation == "continue"):
                    TransferData(clientData, conn)
        # Quit
        else:
            print("Connection has ended, goodbye")
            break

    conn.close()

Server()