# =====================================================================================================================
#
# =====================================================================================================================

# Imports
import socket
import sys
import os

#Global Variable
FORMAT = "utf-8"
BUFFER=1024

# == Download =========================================================================================================

def Download(upFile, fileSize, client):
    # Sends confirmation to continue
    client.send("continue".encode(FORMAT))
    print("\t[Server] - Sends confirmation to continue")

    # Opens download file to write contents on it
    newFile = open("upload_" + upFile, 'w')

    # Receives file's content
    fileContent = client.recv(BUFFER).decode(FORMAT)
    print("\t[Server] - Receives file's content from client")

    # Current data chunk size
    currDataSize = len(fileContent)

    # Writes content to new file
    newFile.write(fileContent)

    # If content exceeds 1024bytes, keep receiving and writing
    while currDataSize < int(fileSize):
        fileContent = client.recv(BUFFER).decode(FORMAT)
        print("\t[Server] - Receives more file's content from client")
        currDataSize += len(fileContent)
        newFile.write(fileContent)
    print("\t[Server] - File was received")






# == TransjerData =====================================================================================================

def TransferData(userFile, client):
    # Open file and read bytes
    with open(userFile, 'r') as File:
        # Start reading file
        bytesSend = File.read(BUFFER)

        # Send what's being read to Client
        client.send(bytesSend.encode(FORMAT))
        print("\t[Server] - Sends file's content to client")

        # If file content exceeds 1024 bytes
        while bytesSend != "":
            bytesSend = File.read(BUFFER)
            client.send(bytesSend.encode(FORMAT))
    print("\t[Server] - The file was successfully transferred")







# == DoesExist ========================================================================================================

def DoesExist(userFile, client):
    # Checks if path exists
    if (os.path.isfile(userFile)):
        userFileSize = str(os.path.getsize(userFile))
        print("\t[Server] - A file of [" + str(userFileSize) + "] bytes was sent to client")
        client.send(userFileSize.encode(FORMAT))
        return True
    return False





# == Server ===========================================================================================================

def Server():
    # Variables
    SERV_PORT = int(sys.argv[1])                                        # Port number
    SERVER = socket.gethostbyname(socket.gethostname())                 # Server's IP address
    SERV_SOCKET = socket.socket(socket.AF_INET, socket.SOCK_STREAM)     # Server's Socket
    SERV_SOCKET.bind((SERVER, SERV_PORT))                               # Bind the Server with Port Number
    QUIT = 'q'                                                          # input to end connection

    # Pepare for possible connections
    SERV_SOCKET.listen(1)
    print("Server [" + str(SERVER) + "] is searching for connections")
    # Gets Info from the client
    conn, address = SERV_SOCKET.accept()
    print(" Client with IP address [" + str(address) + "] is connected")

    # Let client communicate with Server
    while True:
        # Server receives data from Client
        clientData = conn.recv(BUFFER).decode(FORMAT)

        # g(download),p(upload),l(ls),n(nonexistent)
        code = clientData[0]
        clientData = clientData[1:]

        # If code is n, then file does not exist
        if (code == 'n'):
            print("\t[Server] - Confirmation from Client states that file does not exist")
            continue
        # If code is p (upload to server) or g (download from server)
        if ((code == 'p') or (code=='g')):
            print("\t[Server] - Receives file's name with code")
        # If code is l, then provide a list to Client of Server's files/directories
        elif (code == 'l'):
            print ("\t[Server] - Preparing files' names to be sent")

        # If client does not send quit, download, upload, or ls
        if (code != QUIT):
            # If client wants to download a file
            if (code == 'g'):
                if not DoesExist(clientData, conn):
                    print("\t[Server] - File does not exist")
                    conn.send("nonexistent".encode(FORMAT)) 
                else:
                    # if client wants to continue, send content of file
                    confirmation = conn.recv(BUFFER).decode(FORMAT)
                    print("\t[Server] - Receives confirmation to continue")
                    if (confirmation == "continue"):
                        TransferData(clientData, conn)

            # If client wants to upload a file
            if (code == 'p'):
                conn.send("continue".encode(FORMAT))
                print("\t[Server] - Sends confirmation to continue")
                fileSize = conn.recv(BUFFER).decode(FORMAT)
                print("\t[Server] - A file of [" + fileSize + "] is going to be uploaded to the server")
                Download(clientData, fileSize, conn)

            # If client wants to display the Server's files
            if (code == 'l'):
                listFile = os.listdir()
                list = ""
                for i in listFile:
                    list = list + i + " "

                # Sends list of files to Client
                conn.send(list.encode(FORMAT))
                print("\t[Server] - Sends the list of files in the directory")

            #if upload file does not exist
            if(code == 'n'): 
                print("\t[Server] - File was nonexistent")
        # Quit
        else:
            print("\t[Server] - Connection has ended, goodbye")
            break

    conn.close()

Server()
