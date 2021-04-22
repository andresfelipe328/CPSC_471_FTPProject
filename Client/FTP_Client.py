# =====================================================================================================================
#
# =====================================================================================================================

import socket
import os
import sys
import math

# Global Variables
FORMAT = "utf-8"
BUFFER= 1024

# == Download =========================================================================================================

def Download(downFile, CLIENT_SOCKET):
    # Variables
    percentage = 0
    percentTracker = 1

    # Sends the name of file to Server
    print("\t[Client] - Sends file")
    CLIENT_SOCKET.send(downFile.encode(FORMAT))

    # Receives size of data
    fileSize = CLIENT_SOCKET.recv(BUFFER).decode(FORMAT)
    
    # File does not exist
    if (fileSize=="nonexistent"): 
        #CLIENT_SOCKET.send("quit".encode(FORMAT))
        print("\t[Client] - Confirmation from Server states that file does not exist")
        return
        # Closes connection
        CLIENT_SOCKET.close()

    # File does exist, then start writing to new file    
    else:
        # Confirms size of data
        CLIENT_SOCKET.send("continue".encode(FORMAT))
        print("\t[Client] - Sends confirmation to continue")

        # Opens download file to write contents on it
        newFile = open("download_" + downFile[1:], 'wb')

        # Receives file's content
        fileContent = CLIENT_SOCKET.recv(BUFFER)
        print("\t[Client] - Receiving file's content")

        # Current data chunk size
        currDataSize = len(fileContent)

        # Writes content to new file
        newFile.write(fileContent)

        # If content exceeds 1024 bytes, keep receiving and writing in blocks of 1024 bytes
        while currDataSize < int(fileSize):
            # Calculates current transmission percentange
            percentage = (currDataSize / int(fileSize)) * 100
            percentage = math.floor(percentage)

            # Receives data and writes it on new file
            fileContent = CLIENT_SOCKET.recv(BUFFER)
            newFile.write(fileContent)
            CLIENT_SOCKET.send("continue".encode((FORMAT)))
            if (percentage == 20 and percentTracker == 1):
                print("\t\t[Client] - 20% recieved from Server")
                percentTracker += 1
            if (percentage == 40 and percentTracker == 2):
                print("\t\t[Client] - 40% recieved from Server")
                percentTracker += 1
            if (percentage == 60 and percentTracker == 3):
                print("\t\t[Client] - 60% recieved from Server")
                percentTracker += 1
            if (percentage == 80 and percentTracker == 4):
                print("\t\t[Client] - 80% recieved from Server")
                percentTracker += 1
            if (percentage == 99 and percentTracker == 5):
                print("\t\t[Client] - 100% recieved from Server")
                percentTracker += 1

            currDataSize += len(fileContent)

        print("\t[Client] - The file was received successfully")






# == Upload ===========================================================================================================

def Upload(upFile, CLIENT_SOCKET):
    # Variable
    upFileSize = str(os.path.getsize(upFile))
    percentage = 0
    percentTracker = 1

    # Confirmation from Server
    confirmation = CLIENT_SOCKET.recv(BUFFER).decode(FORMAT)
    print("\t[Client] - Receives confirmation from server to continue")

    # Open file and read bytes
    with open(upFile, 'rb') as File:
        # Start reading file
        bytesSend = File.read(BUFFER)

        # Send what's being read to Client
        CLIENT_SOCKET.send(bytesSend)
        print("\t[Client] - Sends file's content to server")

        # Keeps track of current bytes 
        bytesSendSize = len(bytesSend)

        # If file content exceeds 1024 bytes
        while bytesSendSize < int(upFileSize):
            # Calculates current transmission percentage
            percentage = (bytesSendSize / int(upFileSize)) * 100
            percentage = math.floor(percentage)

            # Reads data and sends it to Server
            bytesSend = File.read(BUFFER)
            CLIENT_SOCKET.send(bytesSend)

            if (percentage == 20 and percentTracker == 1):
                print("\t\t[Client] - 20% sent to Server")
                percentTracker += 1
            if (percentage == 40 and percentTracker == 2):
                print("\t\t[Client] - 40% sent to Server")
                percentTracker += 1
            if (percentage == 60 and percentTracker == 3):
                print("\t\t[Client] - 60% sent to Server")
                percentTracker += 1
            if (percentage == 80 and percentTracker == 4):
                print("\t\t[Client] - 80% sent to Server")
                percentTracker += 1
            if (percentage == 99 and percentTracker == 5):
                print("\t\t[Client] - 100% sent to Server")
                percentTracker += 1
        
            bytesSendSize += len(bytesSend)

            
    print("\t[Client] - The file was successfully transferred")





# == DoesExist ========================================================================================================

def DoesExist(upFile, CLIENT_SOCKET):
    # Checks if path exists
    if (os.path.isfile(upFile[1:])):
        # Send file name to server
        CLIENT_SOCKET.send(upFile.encode(FORMAT))
        print("\t[Client] - Sends file's name plus code")
        upFile = upFile[1:]

        # Confirmation from Server
        confirmation = CLIENT_SOCKET.recv(BUFFER).decode(FORMAT)
        print("\t[Client] - Receives confirmation from server to continue")

        # Once confirmed, send size of file
        if (confirmation == "continue"):
            # Send size of File
            userFileSize = str(os.path.getsize(upFile))
            CLIENT_SOCKET.send(userFileSize.encode(FORMAT))
            print("\t[Client] - Sends file's size to Server")
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

    while True:
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
                print("\t[Client] - File does not exist")

                # Sends confirmation that it does not exist
                CLIENT_SOCKET.send("nonexistent".encode(FORMAT))
            # Upload to server
            else:
                Upload(upFile[1:], CLIENT_SOCKET)
            
        # User wants to list files on the server
        elif (comm == "ls"):
            CLIENT_SOCKET.send(comm.encode(FORMAT))
            print("\t[Client] - Request to Server to display file list")
            listFiles = CLIENT_SOCKET.recv(BUFFER).decode(FORMAT)
            print("\t[Client] - These are the files from Server:")
            List= listFiles.split()
            for file in List:
                print("\t\t* "+file)

        # User wants to end connection
        elif (comm == QUIT):
            # Sends QUIT to end connection
            CLIENT_SOCKET.send(comm.encode(FORMAT))
            # Closes connection
            CLIENT_SOCKET.close()
            break

Client()
