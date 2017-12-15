import socketserver
import json
import time

host = 'localhost'
port = 8883

LOCK_TIMEOUT = 60
LOCK_MAPPINGS = {} 

def lockExists(filename):
    return filename in LOCK_MAPPINGS

def getLocks(filename):
    if lockExists(filename):
        return LOCK_MAPPINGS[filename]
    else:
        return None

def deleteLock(filename):
    del LOCK_MAPPINGS[filename]

def addLock(filename, timestamp, timeout):
    LOCK_MAPPINGS[filename] = {"timestamp": timestamp, "timeout": timeout}

class ThreadedHandler(socketserver.BaseRequestHandler):
    def handle(self):
        msg = self.request.recv(1024)

        msg = json.loads(msg)
        requestType = msg['request']

        print ("Request type = " + requestType)
        response = ""
        if requestType == "checklock":
            if lockExists(msg['filename']):
                print ("file locked")
                timestamp = time.time()
                checkFile = getLocks(msg['filename'])

                if checkFile['timestamp']+checkFile['timeout'] < timestamp:
                    deleteLock(msg['filename'])
                    response = json.dumps({
                        "response": "unlocked"})

                elif msg['clientid'] == checkFile['clientid']:
                    print("file locked")
                    response = json.dumps({
                        "response": "lock owned",
                        "filename": msg['filename'],
                        "timestamp": fs['timestamp'],
                        "timeout": fs['timeout']
                    })
                else:
                    print ("file locked")
                    response = json.dumps({
                        "response": "locked",
                        "filename": msg['filename'],
                        "timestamp": checkFile['timestamp'],
                        "timeout": checkFile['timeout']
                    })
            else:
                response = json.dumps({
                    "response": "unlocked"
                })
        elif requestType == "getlock":
            if lockExists(msg['filename']):
                print ("get lock")
                checkFile = getLocks(msg['filename'])
                timestamp = time.time()

                if checkFile['timestamp']+checkFile['timeout'] < timestamp:
                    deleteLock(msg['filename'])
                    addLock(msg['filename'], timestamp, LOCK_TIMEOUT)
                    response = json.dumps({
                        "response": "lock granted",
                        "filename": msg['filename'],
                        "timestamp": fs['timestamp'],
                        "timeout": fs['timeout']})

                elif msg['clientid'] == checkFile['clientid']:
                    print("file locked")
                    response = json.dumps({
                        "response": "lock granted again",
                        "filename": msg['filename'],
                        "timestamp": checkFile['timestamp'],
                        "timeout": checkFile['timeout']
                    })

                else:
                    print ("getlock: locked")
                    response = json.dumps({
                            "response": "locked",
                            "filename": msg['filename'],
                            "timestamp": fs['timestamp'],
                            "timeout": fs['timeout']})
            else:
                timestamp = time.time()
                addLock(msg['filename'], timestamp, LOCK_TIMEOUT)

                response = json.dumps({
                    "response": "lockgranted",
                    "filename": msg['filename'],
                    "timestamp": timestamp,
                    "timeout": LOCK_TIMEOUT
                })
        else:
            response = json.dumps({"response": "Error", "error": requestType+" is not a valid request"})

        self.request.sendall(response.encode('utf-8'))

class LockingServer(socketserver.ThreadingMixIn, socketserver.TCPServer):
    pass

if __name__ == '__main__':
    address = (host, port)
    server = LockingServer(address, ThreadedHandler)
    print("Locking Server Running")
    server.serve_forever()
