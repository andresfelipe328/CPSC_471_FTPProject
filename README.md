# CPSC_471_FTPProject
* https://github.com/andresfelipe328/CPSC_471_FTPProject

## Member's Information:
* Andres F. Romero N. - andresfelipe328@csu.fullerton.edu
* Edward S. Le - edwardl@csu.fullerton.edu
* Vinh Tran - kimvinh@csu.fullerton.edu
* Desirae Prather - DesiraePrather@csu.fullerton.edu
* Rebecca Lee - becca.lee@csu.fullerton.edu

## Programming Language
* Python
* OS to execute code: Linux/Tuffix

## How to Execute:
1. Make sure all related files of Server are in the folder 'Server'
2. Make sure all related files of Client are in the folder 'Client'
3. Create two terminal windows.
   Make sure that the working directory of each terminal window is at the folder of 'Server' or 'Client'
   ```
   # For example:
   The working directory of 'Server' terminal window:
   /Downloads/CPSC_471_FTPProject/Server$

   The working directory of 'Client' terminal window:
   /Downloads/CPSC_471_FTPProject/Client$
   ```
4. First, run the server by commanding **python3 FTP_Server.py {your port number}** on a (Server) terminal window.
   ```
   # For example:
   $ python3 FTP_Server.py 12345
   
   # Result from Server side:
   Server [127.0.1.1] is searching for connections
    Client with IP address [('127.0.0.1', 41252)] is connected
   ```
4. Second, run the client by commanding **python3 FTP_Client.py {your system's IP address} {your corresponding server's port number}** on a (Client) terminal window.
   ```
   # For example:
   $ python3 FTP_Client.py 127.0.0.1 12345
   
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
## Program Details:
* This program works with:
   * txt files
   * png files
   * mp3 files
   * mp4 files
* Both, the Server and Client folder, contain these types of file to begin testing. Get files (download) will have a prefix of "download_" and put files (upload) will have a prefix of "upload_".
* When transmitting files larger than 1024 bytes, both, the server and the client, will display transmission percentage in multiples of 20. 
