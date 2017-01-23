#  coding: utf-8 
import SocketServer, mimetypes, os

# Copyright 2013 Abram Hindle, Eddie Antonio Santos
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
# some of the code is Copyright © 2001-2013 Python Software
# Foundation; All Rights Reserved
#
# http://docs.python.org/2/library/socketserver.html
#
# run: python freetests.py

# try: curl -v -X GET http://127.0.0.1:8080/

class MyWebServer(SocketServer.BaseRequestHandler):
    
    def getMethod(self):
        return self.data[0]
    
    def getFilePath(self):
        self.filePath = os.path.join(os.getcwd(), "www" + self.data[1])
        if os.path.exists(self.filePath):
            return True
        else:
            return False
    
    
    def isdirectory(self):
        if os.path.isdir(self.filePath):
            self.filePath += "index.html"
        return
    
    def getFileType(self):
        self.fileType = mimetypes.guess_type(self.filePath)[0]
        return

    def setupHeader(self):
        self.header = "HTTP/1.1 200 OK\r\nContent-type:" + self.fileType + ";\r\n\r\n"
        return    
    
    def setup404(self):
        self.header = "HTTP/1.1 404 Not Found\r\n\r\n"
        return
    
    def setup405(self):
        self.header = "HTTP/1.1 405 Method Not Allowed\r\n\r\n"
        return
    
    def readFile(self, fileName):
        if fileName == "404":
            file = open("www/404.html")
        elif fileName == "405":
            file = open("www/405.html")
        else:
            file = open(self.filePath)
        
        self.file = file.read()
        file.close()
        return    
    
    def serveFile(self):
        self.request.sendall(self.header + self.file)
        return

    def handle(self):
        self.data = self.request.recv(1024).strip().split(" ")
        print ("Got a request of: %s\n" % self.data)
        
        if self.getMethod() != "GET":
            self.setup405()
            self.readFile("405")
        elif self.getFilePath():
            self.isDirectory()
            self.getFileType()
            self.setupHeader()
            self.readFile(self.fileName)
        else:
            self.setup404()
            self.readFile("404")
        
        self.serveFile()

if __name__ == "__main__":
    HOST, PORT = "localhost", 8080

    SocketServer.TCPServer.allow_reuse_address = True
    # Create the server, binding to localhost on port 8080
    server = SocketServer.TCPServer((HOST, PORT), MyWebServer)

    # Activate the server; this will keep running until you
    # interrupt the program with Ctrl-C
    server.serve_forever()


