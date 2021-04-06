# =====================================================================================================================
#
# =====================================================================================================================

import socket
import sys


def Client():
    # Variables
    CLIENT = socket.gethostbyname(sys.argv[1])                              # Client's IP Address
    CLIENT_PORT = int(sys.argv[2])                                          # Port Number
    CLIENT_SOCKET = socket.socket(socket.AF_INET, socket.SOCK_STREAM)       # Client's Socket
    bytesSent = 0                                                           # Data Sent Counter
    FORMAT = "utf-8"                                                        # format to send/receive data
    QUIT = "quit"                                                           # Ends connection with Server

    # Begin connection
    CLIENT_SOCKET.connect((CLIENT, CLIENT_PORT))

    # Prompts the user to download, upload, or ls
    comm = input("FTP -> ")
    
    # User wants to download a file from server
    if (comm[:3] == "get"):
        # Gets the name of file
        downFile = comm[4:]
        # Sends the name of file to Server
        CLIENT_SOCKET.send(downFile.encode(FORMAT))
        # Gets the size of the file
        downFileSize = CLIENT_SOCKET.recv(1024).decode(FORMAT)
        print(downFileSize)
        # Opens the file and adds a prefix
        downFile = open("download_" + downFile, 'w')
        # Receives file's content
        data = CLIENT_SOCKET.recv(1024).decode(FORMAT)
        print(data)
        # Gets first chunk of data
        totalData = len(data)
        print(totalData)
        # Writes content on download_file
        downFile.write(data)
        # If data exceeds buffer continue until all data is written in download_file
        #while totalData < int(downFileSize):
        #    data = CLIENT_SOCKET.recv(1024)
        #    totalData += len(data)
        #    downFile.write(data)

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