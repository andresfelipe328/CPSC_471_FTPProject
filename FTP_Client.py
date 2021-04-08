# =====================================================================================================================
#
# =====================================================================================================================

import socket
import os
import sys

# Global Variables
FORMAT = "utf-8"


# == Download =========================================================================================================

def Download(downFile, CLIENT_SOCKET):
    # Sends the name of file to Server
    print("    [Client] - Sends file")
    CLIENT_SOCKET.send(downFile.encode(FORMAT))

    # Receives size of data
    fileSize = CLIENT_SOCKET.recv(1024).decode(FORMAT)
    print("    [Client] - Receives data")

    # Confirms size of data
    CLIENT_SOCKET.send("continue".encode(FORMAT))
    print("    [Client] - Sends confirmation to continue")

    # Opens download file to write contents on it
    newFile = open("download_" + downFile[1:], 'w')

    # Receives file's content
    fileContent = CLIENT_SOCKET.recv(1024).decode(FORMAT)
    print("    [Client] - Receiving file's content")

    # Current data chunk size
    currDataSize = len(fileContent)

    # Writes content to new file
    newFile.write(fileContent)

    # If content exceeds 1024bytes, keep receiving and writing
    while currDataSize < int(fileSize):
        fileContent = CLIENT_SOCKET.recv(1024).decode(FORMAT)
        print("    [Client] - Receiving more data")
        currDataSize += len(fileContent)
        newFile.write(fileContent)
    print("    [Client] - File was received")






# == Upload ===========================================================================================================

def Upload(upFile, CLIENT_SOCKET):
    # Confirmation from Server
    confirmation = CLIENT_SOCKET.recv(1024).decode(FORMAT)
    print("    [Client] - Receives confirmation from server to continue")

    # Open file and read bytes
    with open(upFile, 'r') as File:
        # Start reading file
        bytesSend = File.read(1024)

        # Send what's being read to Client
        CLIENT_SOCKET.send(bytesSend.encode(FORMAT))
        print("    [Client] - Sends file's content to server")

        # If file content exceeds 1024 bytes
        while bytesSend != "":
            bytesSend = File.read(1024)
            CLIENT_SOCKET.send(bytesSend.encode(FORMAT))
            print("    [Client] - Sends more file's content to server")
    print("    [Client] - The file was successfully transferred")





# == DoesExist ========================================================================================================

def DoesExist(upFile, CLIENT_SOCKET):
    if (os.path.isfile(upFile[1:])):

        # Send file name to server
        CLIENT_SOCKET.send(upFile.encode(FORMAT))
        print("    [Client] - Sends file's name plus code")
        upFile = upFile[1:]
        confirmation = CLIENT_SOCKET.recv(1024).decode(FORMAT)
        print("    [Client] - Receives confirmation from server to continue")
        if (confirmation == "continue"):
            userFileSize = str(os.path.getsize(upFile))
            CLIENT_SOCKET.send(userFileSize.encode(FORMAT))
            print("    [Client] - Sends file's size to Server")
        return True
    return False





# == Client ===========================================================================================================

def Client():
    # Variables
    CLIENT = socket.gethostbyname(sys.argv[1])                              # Client's IP Address
    CLIENT_PORT = int(sys.argv[2])                                          # Port Number
    CLIENT_SOCKET = socket.socket(socket.AF_INET, socket.SOCK_STREAM)       # Client's Socket
    QUIT = "quit"                                                           # Ends connection with Server

    # Begin connection
    CLIENT_SOCKET.connect((CLIENT, CLIENT_PORT))

    # Prompts the user to download, upload, or ls
    comm = input("FTP -> ")

    # User wants to download a file from server
    if (comm[:3] == "get"):
        # Gets the name of file and adds function code
        downFile = 'g' + comm[4:]
        # Start downloading
        Download(downFile, CLIENT_SOCKET)

    # User wants to upload a file to server
    elif (comm[:3] == "put"):
        # Gets the name of the file and adds function code
        upFile = 'p' + comm[4:]
        # If file does not exist
        if not DoesExist(upFile, CLIENT_SOCKET):
            print("File does not exist")
        # Upload to server
        else:
            Upload(upFile[1:], CLIENT_SOCKET)

    # User wants to list files on the server
    elif (comm == "ls"):
        CLIENT_SOCKET.send(comm.encode(FORMAT))
        list = CLIENT_SOCKET.recv(1024).decode(FORMAT)
        print(list)

    # User wants to end connection
    elif (comm[:4] == "quit"):
        # Sends QUIT to end connection
        CLIENT_SOCKET.send(QUIT.encode(FORMAT))
        #CLIENT_SOCKET.close()
        CLIENT_SOCKET.close()

Client()
