# Python 3 server example
from http.server import BaseHTTPRequestHandler, HTTPServer
import time
import os
import sys
import json
from chronometer import Chronometer

print("Starting NoMoskito! server ...")
with Chronometer() as t_:
    def recreate_conf():
        with open("server.conf", "w+") as file:
            file.write("host_name=\"localhost\"\nport=8080")
            file.close()
        print("server.conf file created. Please check it before launching the server.")
        sys.exit()

    print("Loading config ...")
    with Chronometer() as t:
        try:
            try:
                with open("server.conf", "r") as file:
                    lines = file.readlines()
                    for x in lines:
                        exec(x)
            except:
                print("Failed to read conf file !")
                recreate_conf()
        except:
            recreate_conf()
    with open("index.html", "r") as file:
        index_lines = file.readlines()
        file.close()
    print('Loading config took {:.3f} seconds.'.format(float(t)))


    class MyServer(BaseHTTPRequestHandler):
        def do_GET(self):
            if self.path == "/get/":
                self.send_response(200)  # return 10 best scores
                self.send_header("Content-type", "application/json")
                self.end_headers()
            else:
                self.send_response(200)  # 200 = successful
                self.send_header("Content-type", "text/html")
                self.end_headers()
                for line in index_lines:
                    self.wfile.write(bytes(line, "utf-8"))


    if __name__ == "__main__":
        webServer = HTTPServer((host_name, port), MyServer)
        print("Server started http://%s:%s Do KeyBoardInterrupt to stop" % (host_name, port))
        print("Starting server took {:.3f} seconds.".format(float(t)))

        try:
            webServer.serve_forever()
        except KeyboardInterrupt:
            pass

        webServer.server_close()
        print("Server stopped. (Server ran for {:.3f} seconds.)".format(float(t)))
