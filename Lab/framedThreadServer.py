#! /usr/bin/env python3
import sys, os, socket, params, time, re
import threading
from framedSock import FramedStreamSock

switchesVarDefaults = (
    (('-l', '--listenPort') ,'listenPort', 50001),
    (('-d', '--debug'), "debug", False), # boolean (set if present)
    (('-?', '--usage'), "usage", False), # boolean (set if present)
    )

progname = "echoserver"
paramMap = params.parseParams(switchesVarDefaults)

debug, listenPort = paramMap['debug'], paramMap['listenPort']

if paramMap['usage']:
    params.usage()

lsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # listener socket
bindAddr = ("127.0.0.1", listenPort)
lsock.bind(bindAddr)
lsock.listen(5)
print("listening on:", bindAddr)
lock = threading.Lock()
class ServerThread(threading.Thread):
    requestCount = 0            # one instance / class
    def __init__(self, sock):
        threading.Thread.__init__(self, daemon=True)
        self.sock = sock
        self.start()
    def run(self):
        with lock:
            while True:
                dataIn = self.sock.recv(100)
                fileSize, fileName = dataIn.decode().split(':')
                print(fileSize+", "+fileName)
                if os.path.isfile(fileName):
                    i = 2
                    dataIn = None
                    fileName, fileExt = fileName.split('.')
                    while os.path.isfile(fileName+"."+fileExt):
                        fileName = fileName.split('(')[0]
                        fileName = fileName+"("+str(i)+")"
                        i+=1
                if int(fileSize) > 0:
                    f = open(fileName+"."+fileExt, 'wb')
                    self.sock.send(("READY TO RECEIVE").encode())
                    dataIn = self.sock.recv(100)
                    totalBytesRecvd = len(dataIn)
                    f.write(dataIn)

                    while totalBytesRecvd < int(fileSize):
                        dataIn = self.sock.recv(100)
                        totalBytesRecvd += len(dataIn)
                        f.write(dataIn)

                    self.sock.send(("file transfer complete").encode())

                else:
                     self.sock.send(("EMPTY FILE").encode())


while True:
    sock, addr = lsock.accept()
    ServerThread(sock)
