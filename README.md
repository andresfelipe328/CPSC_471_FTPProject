# CPSC_471_FTPProject

## Member's Information:
* Andres F. Romero N. - andresfelipe328@csu.fullerton.edu
* Edward S. Le - edwardl@csu.fullerton.edu
* Vinh Tran - kimvinh@csu.fullerton.edu
* Desirae Prather - DesiraePrather@csu.fullerton.edu
* Team member 5

## Programming Language
* Python
* OS to execute code: Linux/Tuffix

## How to Execute:
1. Make sure all files are in the same directory
2. Create two terminal windows
3. First, run the server by commanding **python3 FTP_Server.py {your port number}** on a terminal window.
   ```
   # For example:
   python3 FTP_Server.py 12345
   
   # Result from Server side:
   Server [127.0.1.1] is searching for connections
    Client with IP address [('127.0.0.1', 41252)] is connected
   ```
4. Second, run the client by commanding **python3 FTP_Client.py {your system's IP address} {your corresponding server's port number}** on another terminal window.
   ```
   # For example:
   python3 FTP_Client.py 127.0.0.1 12345
   
   # Result from Client side:
   FTP ->
   ```

## How to Use:
- During the connection, Client is prompted to do by commanding:
  ```
    1. get <filename.txt> // Downloads a file from server. Have a ws between get and file.	 
    2. put <filename.txt> // Uploads a file to server. Have a ws between put and file
    3. ls                 // Provides a list of files in the Server
    4. quit               // Disconnects from the server and exits
  ```
