# Python 3 server example
from http.server import BaseHTTPRequestHandler, HTTPServer
import time
import os
import sys

def recreate_conf():
    with open("server.conf", "w+") as file:
        file.write("host_name=\"localhost\"\nport=8080")
        file.close()
    print("server.conf file created. Please check it before launching the server.")
    sys.exit()

try:
    os.rename("server.conf", "serverini.py")
    try:
        from serverini import *
    except:
        recreate_conf()
    os.rename("serverini.py", "server.conf")
except:
    recreate_conf()

try:
    os.removedirs("__pycache__")
except:
    pass

class MyServer(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)  # 200 = successful
        self.send_header("Content-type", "text/html")
        self.end_headers()
        self.wfile.write(bytes("<html><head><title>https://pythonbasics.org</title></head>", "utf-8"))
        self.wfile.write(bytes("<p>Request: %s</p>" % self.path, "utf-8"))
        self.wfile.write(bytes("<body>", "utf-8"))
        self.wfile.write(bytes("<p>This is an example web server.</p>", "utf-8"))
        self.wfile.write(bytes("</body></html>", "utf-8"))

if __name__ == "__main__":
    webServer = HTTPServer((host_name, port), MyServer)
    print("Server started http://%s:%s" % (host_name, port))

    try:
        webServer.serve_forever()
    except KeyboardInterrupt:
        pass

    webServer.server_close()
    print("Server stopped.")

try:
    os.removedirs("__pycache__")
except:
    pass
