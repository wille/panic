import argparse
import threading
import platform
import socket
from http.server import HTTPServer, BaseHTTPRequestHandler

argparse = argparse.ArgumentParser()
argparse.add_argument("-b", "--bport", dest = "buttonport", help = "Port where HTTP server will listen")
argparse.add_argument("-s", "--sport", dest = "signalport", help = "Port where UDP server will listen and broadcast signal to")
argparse.add_argument("-k", "--key", dest = "key", help = "Signal password, preventing unauthorized machines to trigger panic")
args = argparse.parse_args()

global button_port
button_port = int(args.buttonport or 8080)

global signal_port
signal_port = int(args.signalport or 1301)

global key
key = args.key

if key is None:
    raise Exception("No key specified")


def getBroadcastAddresses():
    addresses = []
    
    return addresses

def createSocket():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    return s

def broadcastListener():
    s = createSocket()
    s.bind(("", signal_port))

    while True:
        try:
            message, address = s.recvfrom(1024)
            if message.decode() == key:
                broadcast()
        except:
            pass

def broadcast():
    addresses = getBroadcastAddresses()
    for address in addresses:
        s = createSocket()
        s.sendto(key.encode(), (address, signal_port))
        s.close()

class HTTPHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        path = self.path[1:]
        print("Got request: " + path);

def createServer():
    server = HTTPServer(("", button_port), HTTPHandler)
    server.serve_forever()

if __name__ == "__main__":
    print("Detected system: " + platform.system())

    threading.Thread(name="UDP thread", target=broadcastListener).start()
    threading.Thread(name="HTTP thread", target=createServer).start()