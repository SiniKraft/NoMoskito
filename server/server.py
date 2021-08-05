# NoMoskito! Server by SiniKraft. Check LICENSE.txt !
from http.server import BaseHTTPRequestHandler, HTTPServer
import time
import os
import sys
import json
from chronometer import Chronometer
import threading

print("Starting NoMoskito! server ...")
with Chronometer() as t_:
    def recreate_conf():
        with open("server.conf", "w+") as file:
            file.write("host_name=\"localhost\"\nport=8080\n# By changig the value of accept_license"
                       " to True you have read and accept the License, written in LICENSE.txt.\naccept_license=False")
            file.close()
        print("server.conf file created. Please check it before launching the server.")
        sys.exit()


    def build_main_dict(scores):
        new_dict = {'1': [0, ""], '2': [0, ""], '3': [0, ""], '4': [0, ""], '5': [0, ""], '6': [0, ""], '7': [0, ""],
                    '8': [0, ""], '9': [0, ""], '10': [0, ""], }
        for score in scores:
            if score[0] > new_dict['1'][0]:
                new_dict['10'] = new_dict['9']
                new_dict['9'] = new_dict['8']
                new_dict['8'] = new_dict['7']
                new_dict['7'] = new_dict['6']
                new_dict['6'] = new_dict['5']
                new_dict['5'] = new_dict['4']
                new_dict['4'] = new_dict['3']
                new_dict['3'] = new_dict['2']
                new_dict['2'] = new_dict['1']
                new_dict['1'] = score
            elif score[0] > new_dict['2'][0]:
                new_dict['10'] = new_dict['9']
                new_dict['9'] = new_dict['8']
                new_dict['8'] = new_dict['7']
                new_dict['7'] = new_dict['6']
                new_dict['6'] = new_dict['5']
                new_dict['5'] = new_dict['4']
                new_dict['4'] = new_dict['3']
                new_dict['3'] = new_dict['2']
                new_dict['2'] = score
            elif score[0] > new_dict['3'][0]:
                new_dict['10'] = new_dict['9']
                new_dict['9'] = new_dict['8']
                new_dict['8'] = new_dict['7']
                new_dict['7'] = new_dict['6']
                new_dict['6'] = new_dict['5']
                new_dict['5'] = new_dict['4']
                new_dict['4'] = new_dict['3']
                new_dict['3'] = score
            elif score[0] > new_dict['4'][0]:
                new_dict['10'] = new_dict['9']
                new_dict['9'] = new_dict['8']
                new_dict['8'] = new_dict['7']
                new_dict['7'] = new_dict['6']
                new_dict['6'] = new_dict['5']
                new_dict['5'] = new_dict['4']
                new_dict['4'] = score
            elif score[0] > new_dict['5'][0]:
                new_dict['10'] = new_dict['9']
                new_dict['9'] = new_dict['8']
                new_dict['8'] = new_dict['7']
                new_dict['7'] = new_dict['6']
                new_dict['6'] = new_dict['5']
                new_dict['5'] = score
            elif score[0] > new_dict['6'][0]:
                new_dict['10'] = new_dict['9']
                new_dict['9'] = new_dict['8']
                new_dict['8'] = new_dict['7']
                new_dict['7'] = new_dict['6']
                new_dict['6'] = score
            elif score[0] > new_dict['7'][0]:
                new_dict['10'] = new_dict['9']
                new_dict['9'] = new_dict['8']
                new_dict['8'] = new_dict['7']
                new_dict['7'] = score
            elif score[0] > new_dict['8'][0]:
                new_dict['10'] = new_dict['9']
                new_dict['9'] = new_dict['8']
                new_dict['8'] = score
            elif score[0] > new_dict['9'][0]:
                new_dict['10'] = new_dict['9']
                new_dict['9'] = score
            elif score[0] > new_dict['10'][0]:
                new_dict['10'] = score
        return new_dict


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
    if os.path.isfile("scores.json"):
        with open("scores.json", 'r') as file:
            scores = json.loads(file.read())
            file.close()
    else:
        scores = [[0, ""]]
    print('Loading config took {:.3f} seconds.'.format(float(t)))

    def save_score():
        with open("scores.json", "w+") as file:
            file.write(json.dumps(scores, indent=4))
            file.close()
    if not accept_license:
        print("To start the server, change accept_license value to True in server.conf !")
        sys.exit()

    class MyServer(BaseHTTPRequestHandler):
        def send_custom_error(self, error):
            self.send_response(200)
            self.send_header("Content-type", "application/json")
            self.end_headers()
            self.wfile.write(bytes(json.dumps({'state': 'failed', 'content': error}, indent=4), 'utf-8'))

        def do_GET(self):
            if self.path == "/get/":
                self.send_response(200)  # return 10 best scores
                self.send_header("Content-type", "application/json")
                self.end_headers()
                try:
                    self.wfile.write(bytes(json.dumps({'state': 'success', 'content': build_main_dict(scores)},
                                                      indent=4), 'utf-8'))
                except Exception as e:
                    self.wfile.write(bytes(json.dumps({'state': 'failed', 'content': str(e)}, indent=4), "utf-8"))
            elif self.path == "/":
                self.send_response(200)  # 200 = successful
                self.send_header("Content-type", "text/html")
                self.end_headers()
                for line in index_lines:
                    self.wfile.write(bytes(line, "utf-8"))
            else:
                if '/send/' in self.path and self.path.split("/")[1] == "send":
                    if self.path[-1] == "/":
                        path = self.path
                    else:
                        path = self.path + "/"
                    if len(path.split("/")) == 5:
                        try:
                            username = str(path.split("/")[2])
                            score = int(path.split("/")[3])
                            if not [score, username] in scores:
                                print("Received score : %s by %s !" % (score, username))
                                scores.append([score, username])
                                save_score()
                                self.send_response(200)
                                self.send_header("Content-type", "application/json")
                                self.end_headers()
                                self.wfile.write(bytes(json.dumps({'state': 'success', 'content': None}, indent=4),
                                                       'utf-8'))
                            else:
                                self.send_custom_error("This element already exists in database !")
                        except Exception as e:
                            self.send_custom_error(str(e))
                    else:
                        self.send_custom_error("Missing or too many arguments !")

                else:
                    self.send_response(200)
                    self.send_header("Content-type", "text/html")
                    self.end_headers()
                    self.wfile.write(bytes("<!DOCTYPE html><html lang=\"en\"><head><meta "
                                           "charset=\"utf-8\"/><title>404 Not Found</titl"
                                           "e></head><body><h1>404 Not Found</h1></body></html>", 'utf-8'))


    if __name__ == "__main__":
        webServer = HTTPServer((host_name, port), MyServer)
        print("Server started at 'http://%s:%s' !" % (host_name, port))
        print("Starting server took {:.3f} seconds.".format(float(t)))

        def launch_server():
            try:
                webServer.serve_forever()
            except KeyboardInterrupt:
                pass
            webServer.server_close()
            print("Server stopped. (Server ran for {:.3f} seconds.)".format(float(t)))

        start_srv_thread = threading.Thread(target=launch_server)
        start_srv_thread.start()
        print("Enter stop to stop the server.")
        while True:
            a = input("")
            if a == "stop":
                break
        print("Server stopped. (Server ran for {:.3f} seconds.)".format(float(t)))
        sys.exit()
