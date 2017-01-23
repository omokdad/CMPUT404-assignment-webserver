#  coding: utf-8 
import SocketServer, mimetypes, os

# Copyright 2016 Abram Hindle, Eddie Antonio Santos, Omar Almokdad
# 
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
# 
#     http://www.apache.org/licenses/LICENSE-2.0
# 
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
#
# Furthermore it is derived from the Python documentation examples thus
# some of the code is Copyright © 2001-2016 Python Software
# Foundation; All Rights Reserved
#
# http://docs.python.org/2/library/socketserver.html
# http://docs.python.org/2/library/mimetypes.html
# http://docs.python.org/2/library/os.html
#
#
#
# run: python freetests.py

# try: curl -v -X GET http://127.0.0.1:8080/

class MyWebServer(SocketServer.BaseRequestHandler):
    
    # gets the method that the cliend wants to use. i.e: (GET/PUT/POST...)
    def getMethod(self):
        return self.data[0]
    
    # gets the path to the file or directory that the client wants served
    def getFilePath(self):

        # getting the current directory from Stackoverflow
        # writen by Russell Dias(http://stackoverflow.com/users/322129/russell-dias) 
        # on Stackoverflow (http://stackoverflow.com/questions/5137497/find-current-directory-and-files-directory)
        self.filePath = os.path.join(os.getcwd(), "www" + self.data[1])
        if os.path.exists(self.filePath):
            return True
        else:
            return False
    
    # checks if the path is a directory and directs it to index.html if it is.
    def fixDirectory(self):

        if os.path.isdir(self.filePath):
            self.filePath += "index.html"
        return
    
    # gets the type of the file to be served so the metatata can be usefull
    def getFileType(self):
        
        # getting the mime type from stackoverflow
        # writen by Blender(http://stackoverflow.com/users/464744/blender)
        # on Stackoverflow (http://stackoverflow.com/questions/14412211/get-mimetype-of-file-python)
        self.fileType = mimetypes.guess_type(self.filePath)[0]
        return self.fileType

    # sets up the header if 200 OK 
    def setupHeader(self):
        self.header = "HTTP/1.1 200 OK\r\nContent-type:" + self.fileType + ";\r\n\r\n"
        return    
    
    # sets up the header if 404 Not Found
    def setup404(self):
        self.header = "HTTP/1.1 404 Not Found\r\n\r\n"
        return
    
    # sets up the header if 405 Method not Allowed
    def setup405(self):
        self.header = "HTTP/1.1 405 Method Not Allowed\r\n\r\n"
        return
    
    # reads the file to be served
    def readFile(self, fileName):
        
        # default file for 404
        if fileName == "404":
            file = open("www/404.html")
        # default file for 405 
        elif fileName == "405":
            file = open("www/405.html")
        # file asked by the client
        else:
            file = open(self.filePath)
        
        self.file = file.read()

        # close file after read
        file.close()
        return    
    
    # serve the file with the appropriate header
    def serveFile(self):
        self.request.sendall(self.header + self.file)
        return
    
    # Original provided by Abram Hindle for Assignment 1.
    # Modified by Omar Almokdad
    def handle(self):
        self.data = self.request.recv(1024).strip().split(" ")
        
        # logic of the serving

        # Check for 405
        if self.getMethod() != "GET":
            # Method Not Allowed
            self.setup405()
            self.readFile("405")
        
        # Check for 404
        elif self.getFilePath():
            self.fixDirectory()

            # check for directory 404
            if self.getFileType():
                # file found
                self.setupHeader()
                self.readFile(self.filePath)
            else:
                # index.html not found
                self.setup404()
                self.readFile("404")
        else:
            # file not found
            self.setup404()
            self.readFile("404")
        
        self.serveFile()

# Provided by Abram Hindle for Assignment 1.
if __name__ == "__main__":
    HOST, PORT = "localhost", 8080

    SocketServer.TCPServer.allow_reuse_address = True
    # Create the server, binding to localhost on port 8080
    server = SocketServer.TCPServer((HOST, PORT), MyWebServer)

    # Activate the server; this will keep running until you
    # interrupt the program with Ctrl-C
    server.serve_forever()


