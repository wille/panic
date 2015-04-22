import argparse
import threading
import platform
import socket
import os
import sys
from http.server import HTTPServer, BaseHTTPRequestHandler

argparse = argparse.ArgumentParser()
argparse.add_argument("-b", "--bport", dest = "buttonport", help = "Port where HTTP server will listen")
argparse.add_argument("-s", "--sport", dest = "signalport", help = "Port where UDP server will listen and broadcast signal to")
argparse.add_argument("-k", "--key", dest = "key", help = "Signal password, preventing unauthorized machines to trigger panic")
argparse.add_argument("-v", "--verbose", dest = "verbose", action = "store_true", help = "Verbose")
argparse.add_argument("--startup", dest = "startup", action = "store_true", help = "Will try to add this script to startup")
argparse.add_argument("--debug", dest = "debug", action = "store_true", help = "Do not execute panic actions")
args = argparse.parse_args()

global button_port
button_port = int(args.buttonport or 8080)

global signal_port
signal_port = int(args.signalport or 1301)

global key
key = args.key

global verbose
verbose = args.verbose

global startup
startup = args.startup

global debug
debug = args.debug

if key is None:
    raise Exception("No key specified")

def checkPath():
    pass

def panic():
    print("Shutting down")
    
    if not debug:
        if "win" in sys.platform:
            os.popen("shutdown /p /f")
        elif "darwin" in sys.platform:
            os.popen("shutdown -s now")
        elif "linux" in sys.platform or "bsd" in sys.platform:
            os.popen("poweroff")
            
        if "win" in sys.platform:
            os.popen("truecrypt /d")
        else:
            os.popen("truecrypt -d")

def getBroadcastAddresses():
    addresses = []    
    if "win" in sys.platform:
        raw = os.popen("ipconfig").read()
        for line in raw.split("\n"):
            split = line.split(" : ")
            if len(split) >= 2 and "IPv4" in split[0]:
                ip = split[1]
                ip = ip[:ip.rindex(".")] + ".255"
                addresses.append(ip)
    elif "darwin" in sys.platform or "bsd" in sys.platform:
        raw = os.popen("ifconfig").read()
        for line in raw.split("\n"):
            if "broadcast " in line:
                broadcast = line[line.index("broadcast ") + 10:].strip()
                addresses.append(broadcast)
    elif "linux" in sys.platform:
        if "Bcast:" in os.popen("ifconfig").read():
            raw = os.popen("ifconfig | grep -o \"Bcast:[0-9]*\.[0-9]*\.[0-9]*\.[0-9]*\"").read()
            addresses.append(raw[6:])
        else:
            raw = os.popen("ifconfig | grep -o \"broadcast [0-9]*\.[0-9]*\.[0-9]*\.[0-9]*\"").read()
            addresses.append(raw[10:])
    
    if verbose:
        for address in addresses:
            print("Using broadcast address " + address)
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
                panic()
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
        req = self.path[1:]
        if req == key:
            broadcast()

def createServer():
    server = HTTPServer(("", button_port), HTTPHandler)
    server.serve_forever()

if __name__ == "__main__":
    print("Detected system: " + platform.system())

    threading.Thread(name="UDP thread", target=broadcastListener).start()
    threading.Thread(name="HTTP thread", target=createServer).start()