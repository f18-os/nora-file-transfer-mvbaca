#! /usr/bin/env python3

# Echo client program
import socket, sys, re, os
import params
import threading
import time

switchesVarDefaults = (
    (('-s', '--server'), 'server', "localhost:50001"),
    (('-d', '--debug'), "debug", False), # boolean (set if present)
    (('-?', '--usage'), "usage", False), # boolean (set if present)
    )


progname = "framedClient"
paramMap = params.parseParams(switchesVarDefaults)

server, usage, debug  = paramMap["server"], paramMap["usage"], paramMap["debug"]

if usage:
    params.usage()


try:
    serverHost, serverPort = re.split(":", server)
    serverPort = int(serverPort)
except:
    print("Can't parse server:port from '%s'" % server)
    sys.exit(1)

class ClientThread(threading.Thread):
    def __init__(self, serverHost, serverPort):
        threading.Thread.__init__(self, daemon=False)
        self.serverHost, self.serverPort = serverHost, serverPort
        self.start()
    def run(self):
       sock = None
       for res in socket.getaddrinfo(serverHost, serverPort, socket.AF_UNSPEC, socket.SOCK_STREAM):
           af, socktype, proto, canonname, sa = res
           try:
               print("creating sock: af=%d, type=%d, proto=%d" % (af, socktype, proto))
               sock = socket.socket(af, socktype, proto)
           except socket.error as msg:
               print(" error: %s" % msg)
               sock = None
               continue
           try:
               print(" attempting to connect to %s" % repr(sa))
               sock.connect(sa)
           except socket.error as msg:
               print(" error: %s" % msg)
               sock.close()
               sock = None
               continue
           break

       if sock is None:
           print('could not open socket')
           sys.exit(1)


       #fileName = input("What file would you like to send? ->")
       fileName = "framedThreadClient.py"

       if os.path.isfile(fileName):
           size = os.path.getsize(fileName)
           sock.send((str(size)+":"+fileName).encode())
           serverMsg = sock.recv(100).decode()
           if serverMsg == "READY TO RECEIVE":
               print("Server: "+serverMsg)
               
               with open(fileName, 'rb') as f:
                   bytesToSend = f.read(100)
                   sock.send(bytesToSend)
                   while bytesToSend.decode() != "":
                       bytesToSend = f.read(100)
                       sock.send(bytesToSend)

               print("done sending file")
               print("Server: "+ sock.recv(100).decode())

           elif serverMsg == "EMPTY FILE":
               print("File "+fileName+" is empty")

       else:
           print(fileName+" does not exist")

for i in range(3):
    ClientThread(serverHost, serverPort)

