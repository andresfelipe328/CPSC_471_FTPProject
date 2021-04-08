# =====================================================================================================================
#
# =====================================================================================================================

# Imports
import socket
import sys
import os

#Global Variable
FORMAT = "utf-8"


# == Download =========================================================================================================

def Download(upFile, fileSize, client):
    # Sends confirmation to continue
    client.send("continue".encode(FORMAT))
    print(" [Server] - Sends confirmation to continue")

    # Opens download file to write contents on it
    newFile = open("upload_" + upFile, 'w')

    # Receives file's content
    fileContent = client.recv(1024).decode(FORMAT)
    print(" [Server] - Receives file's content from client")

    # Current data chunk size
    currDataSize = len(fileContent)

    # Writes content to new file
    newFile.write(fileContent)

    # If content exceeds 1024bytes, keep receiving and writing
    while currDataSize < int(fileSize):
        fileContent = client.recv(1024).decode(FORMAT)
        print(" [Server] - Receives more file's content from client")
        currDataSize += len(fileContent)
        newFile.write(fileContent)
    print(" [Server] - File was received")






# == TransjerData =====================================================================================================

def TransferData(userFile, client):
    # Open file and read bytes
    with open(userFile, 'r') as File:
        # Start reading file
        bytesSend = File.read(1024)

        # Send what's being read to Client
        client.send(bytesSend.encode(FORMAT))
        print(" [Server] - Sends file's content to client")

        # If file content exceeds 1024 bytes
        while bytesSend != "":
            bytesSend = File.read(1024)
            client.send(bytesSend.encode(FORMAT))
    print(" [Server] - The file was successfully transferred")







# == DoesExist ========================================================================================================

def DoesExist(userFile, client):
    if (os.path.isfile(userFile)):
        userFileSize = str(os.path.getsize(userFile))
        print(" [Server] - A file of [" + str(userFileSize) + "] bytes was sent to client")
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
        print(" [Server] - Receives file's name with code")
        # g(download),p(upload),l(ls)
        code = clientData[0]
        clientData = clientData[1:]

        # If client does not send quit, download, upload, or ls
        if (clientData != QUIT):
            if (code == 'g'):
                if not DoesExist(clientData, conn):
                    print("File does not exist")
                    break
                else:
                    # if client wants to continue, send content of file
                    confirmation = conn.recv(1024).decode(FORMAT)
                    print(" [Server] - Receives confirmation to continue")
                    if (confirmation == "continue"):
                        TransferData(clientData, conn)
                        break
            if (code == 'p'):
                conn.send("continue".encode(FORMAT))
                print(" [Server] - Sends confirmation to continue")
                fileSize = conn.recv(1024).decode(FORMAT)
                print(" [Server] - A file of [" + fileSize + "] is going to be uploaded to the server")
                Download(clientData, fileSize, conn)
                break

            if (code == 'l'):
                listFile = os.listdir()
                list = ""
                for i in listFile:
                    list = list + i + " "

                conn.send(list.encode(FORMAT))
                print(" [Server] - Sends the list of files in the directory")
                break
        # Quit
        else:
            print("Connection has ended, goodbye")
            break

    conn.close()

Server()
