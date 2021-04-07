# =====================================================================================================================
#
# =====================================================================================================================

import socket
import sys

# Global Variables
FORMAT = "utf-8"


# == Download =========================================================================================================

def Download(downFile, CLIENT_SOCKET):
    # Sends the name of file to Server
    CLIENT_SOCKET.send(downFile.encode(FORMAT))
        
    # Receives size of data
    fileSize = CLIENT_SOCKET.recv(1024).decode(FORMAT)

    # Confirms size of data
    CLIENT_SOCKET.send("continue".encode(FORMAT))
    print("Client is ready to download a [" + str(fileSize + "] bytes file"))

    # Opens download file to write contents on it
    newFile = open("download_" + downFile[1:], 'w')

    # Receives file's content
    fileContent = CLIENT_SOCKET.recv(1024).decode(FORMAT)

    # Current data chunk size
    currDataSize = len(fileContent)

    # Writes content to new file
    newFile.write(fileContent)

    # If content exceeds 1024bytes, keep receiving and writing
    while currDataSize < int(fileSize):
        fileContent = CLIENT_SOCKET.recv(1024).decode(FORMAT)
        currDataSize += len(fileContent)
        newFile.write(fileContent)






# == Upload ===========================================================================================================







# == Client ===========================================================================================================

def Client():
    # Variables
    CLIENT = socket.gethostbyname(sys.argv[1])                              # Client's IP Address
    CLIENT_PORT = int(sys.argv[2])                                          # Port Number
    CLIENT_SOCKET = socket.socket(socket.AF_INET, socket.SOCK_STREAM)       # Client's Socket
    bytesSent = 0                                                           # Data Sent Counter
    QUIT = "quit"                                                           # Ends connection with Server

    # Begin connection
    CLIENT_SOCKET.connect((CLIENT, CLIENT_PORT))

    # Prompts the user to download, upload, or ls
    comm = input("FTP -> ")
    
    # User wants to download a file from server
    if (comm[:3] == "get"):
        # Gets the name of file
        downFile = 'g' + comm[4:]
        # Start Downloading
        Download(downFile, CLIENT_SOCKET)

    # User wants to upload a file to server
    elif (comm[:3] == "put"):
        print("receive")

    # User wants to end connection
    elif (comm[:4] == "quit"):
        # Sends QUIT to end connection
        CLIENT_SOCKET.send(QUIT.encode(FORMAT))
        #CLIENT_SOCKET.close()
    CLIENT_SOCKET.close()

Client()