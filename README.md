# CPSC_471_FTPProject

## Member's Information:
* Andres F. Romero N. - andresfelipe328@csu.fullerton.edu
* Edward S. Le - edwardl@csu.fullerton.edu
* Vinh Tran - kimvinh@csu.fullerton.edu
* Team member 4
* Team member 5

## How to Execute:
1. Make sure all files are in the same directory.
2. Create two terminal windows.
3. First, run FTP_Server: python3 FTP_Server.py 1234 in one window
4. Second, run FTP_Client: python3 FTP_Client.py <your system's IP address> 1234
5. Client is prompted to do:
    a. get <filename.txt> // Downloads a file from server. Have a ws between get and file.
    b. put <filename.txt> // Uploads a file to server. Have a ws between put and file
    c. ls                 // Provides a list of files in the Server
6. Once a "get" or "put" is given, connection ends between client and server
