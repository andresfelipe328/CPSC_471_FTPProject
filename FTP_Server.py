# =====================================================================================================================
#
# =====================================================================================================================

# Imports
import socket
import sys
import os


# == DoesExist ========================================================================================================

def DoesExist(userFile):
    if (os.path.isfile(userFile)):
        return True
    return False




# == Server ===========================================================================================================

def Server():
    # Variables
    SERV_PORT = int(sys.argv[1])                                        # Port number
    SERVER = socket.gethostbyname(socket.gethostname())                 # Server's IP address
    SERV_SOCKET = socket.socket(socket.AF_INET, socket.SOCK_STREAM)     # Server's Socket
    SERV_SOCKET.bind((SERVER, SERV_PORT))                               # Bind the Server with Port Number
    FORMAT = "utf-8"                                                    # format to receive/send data
    QUIT = "quit"                                                       # input to end connection

    # Pepare for possible connections
    SERV_SOCKET.listen(1)
    print("Server [" + str(SERVER) + "] is ready to receive information")

    # Let client connect
    while True:
        # Gets Info from the client
        conn, address = SERV_SOCKET.accept()
        print("Client with IP address [" + str(address) + "] is connected")
        
        # Server receives data from Client
        clientData = conn.recv(1024).decode(FORMAT)

        # If client does not send quit, download, upload, or ls
        if (clientData != QUIT):
            if not DoesExist(clientData):
                print("File does not exist")
        # Quit
        else:
            print("Connection has ended, goodbye")
            break

    conn.close()

Server()