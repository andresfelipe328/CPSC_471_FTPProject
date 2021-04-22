# =====================================================================================================================
#
# =====================================================================================================================

# Imports
import socket
import sys
import os
import math

#Global Variable
FORMAT = "utf-8"
BUFFER= 1024

# == Download =========================================================================================================

def Download(upFile, fileSize, client):
    # Variables
    percentage = 0
    percentTracker = 1

    # Sends confirmation to continue
    client.send("continue".encode(FORMAT))
    print("\t[Server] - Sends confirmation to continue")

    # Opens download file to write contents on it
    newFile = open("upload_" + upFile, 'wb')

    # Receives file's content
    fileContent = client.recv(BUFFER)
    print("\t[Server] - Receives file's content from client")

    # Current data chunk size
    currDataSize = len(fileContent)

    # Writes content to new file
    newFile.write(fileContent)

    # If content exceeds 1024 bytes, keep receiving and writing in blocks of 1024 bytes
    while currDataSize < int(fileSize):
        # Calculates current transmission percentage
        percentage = (currDataSize / int(fileSize)) * 100
        percentage = math.floor(percentage)

        # Receives data and writes it on new file
        fileContent = client.recv(BUFFER)
        newFile.write(fileContent)

        if (percentage == 20 and percentTracker == 1):
            print("\t\t[Server] - 20% received from Client")
            percentTracker += 1
        if (percentage == 40 and percentTracker == 2):
            print("\t\t[Server] - 40% received from Client")
            percentTracker += 1
        if (percentage == 60 and percentTracker == 3):
            print("\t\t[Server] - 60% received from Client")
            percentTracker += 1
        if (percentage == 80 and percentTracker == 4):
            print("\t\t[Server] - 80% received from Client")
            percentTracker += 1
        if (percentage == 99 and percentTracker == 5):
            print("\t\t[Server] - 100% received from Client")
            percentTracker += 1

        currDataSize += len(fileContent)

    print("\t[Server] - The file was received successfully")






# == TransjerData =====================================================================================================

def TransferData(userFile, client):
    # Variables
    percentage = 0
    percentTracker = 1

    # Open file and read bytes
    with open(userFile, 'rb') as File:
        # Start reading file
        bytesSend = File.read(BUFFER)

        # Send what's being read to Client
        client.send(bytesSend)
        print("\t[Server] - Sends file's content to client")

        # Keeps track of bytes send and file's size 
        bytesSendSize = len(bytesSend)
        userFileSize = str(os.path.getsize(userFile))

        # If file content exceeds 1024 bytes
        while bytesSendSize < int(userFileSize):
            # Calculates current transmission percentage 
            percentage = (bytesSendSize / int(userFileSize)) * 100
            percentage = math.floor(percentage)

            # Reads data and sends it to Client
            bytesSend = File.read(BUFFER)
            client.send(bytesSend)

            if (percentage == 20 and percentTracker == 1):
                print("\t\t[Server] - 20% Sent to Client")
                percentTracker += 1
            if (percentage == 40 and percentTracker == 2):
                print("\t\t[Server] - 40% Sent to Client")
                percentTracker += 1
            if (percentage == 60 and percentTracker == 3):
                print("\t\t[Server] - 60% Sent to Client")
                percentTracker += 1
            if (percentage == 80 and percentTracker == 4):
                print("\t\t[Server] - 80% Sent to Client")
                percentTracker += 1
            if (percentage == 99 and percentTracker == 5):
                print("\t\t[Server] - 100% Sent to Client")
                percentTracker += 1

            bytesSendSize += len(bytesSend)

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
                # Confirmation to continue
                conn.send("continue".encode(FORMAT))
                print("\t[Server] - Sends confirmation to continue")

                # Gets size of file
                fileSize = conn.recv(BUFFER).decode(FORMAT)
                print("\t[Server] - A file of [" + fileSize + "] bytes is going to be uploaded to the server")
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
