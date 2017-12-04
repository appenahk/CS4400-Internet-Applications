import SocketServer
import json
import time

Host = "localhost"
Port = 8883

LOCK_TIMEOUT = 60
LOCK_MAPPINGS = {} 

def lockExists(filename):
    return filename in LOCK_MAPPINGS

def getLocks(filename):
    if lockExists(filename):
        return LOCK_MAPPINGS[filename]
    else:
        return None

class ThreadedHandler(SocketServer.BaseRequestHandler):
    def handle(self):
        msg = self.request.recv(1024)


        msg = json.loads(msg)
        requestType = msg['request']

        print "Request type = " + requestType

        response = ""

        if requestType == "checklock":
            if lockExists(msg['filename']):
                print "file locked"
                timestamp = time.time()
  		checkFile = getLocks(msg['filename'])


        elif requestType == "getlock":
            if lockExists(msg['filename']):
                print "Obtain lock"

                
            else:
                
        else:
            response = json.dumps({"response": "Error", "error": requestType+" is not a valid request"})

        self.request.sendall(response)


class LockingServer(SocketServer.ThreadingMixIn, SocketServer.TCPServer):
    pass

if __name__ == '__main__':
    address = (Host, Port)
    server = LockingServer(address, ThreadedHandler)
    server.serve_forever()
