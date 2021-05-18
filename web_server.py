from flask import Flask
from flask_sockets import Sockets
import time
import threading
import socket
import asyncio
from gevent import pywsgi
from geventwebsocket.handler import WebSocketHandler
import socket
import numpy as np


class myServer(threading.Thread):

    def __init__(self,duration):
        threading.Thread.__init__(self)
        self.setDaemon(True)
        self.data={"acc":[],"gyro":[],"mag":[]}
        self.threadID = "ServerThread"
        self.lock = threading.Lock()
        self.duration = duration
        self.IP = None
        self.PORT = None

    def setIP(self,IP):
        self.IP = IP

    def setPort(self,Port):
        self.PORT = Port

    def getIP(self):
        return self.IP

    def getPort(self):
        return self.PORT


    def add_value(self,key,data):
        self.lock.acquire()
        if len(self.data[key]) == 0:
            self.data[key].append(data)
        elif (self.data[key][-1][0] - self.data[key][0][0])/1000000000 < self.duration:
            self.data[key].append(data)
        else:
            self.data[key].pop(0)
            self.data[key].append(data)
        self.lock.release()

    def return_value(self):

        self.lock.acquire()
        temp_data = self.data
        #self.data = {"acc":[],"gyro":[],"mag":[]}
        self.lock.release()

        return temp_data


    def run(self):
        app = Flask(__name__)
        sockets = Sockets(app)
        @sockets.route('/accelerometer')
        def echo_socket(ws):
            while True:
                message = ws.receive()
                msg = [float(n) for n in message.split(",")]
                msg=[time.time_ns()]+msg
                self.add_value("acc",msg)
                ws.send(message)

        @sockets.route('/gyroscope')
        def echo_socket(ws):
            while True:
                message = ws.receive()
                msg = [float(n) for n in message.split(",")]
                msg = [time.time_ns()] + msg
                self.add_value("gyro", msg)
                ws.send(message)

        @sockets.route('/magnetometer')
        def echo_socket(ws):
            while True:
                message = ws.receive()
                msg = [time.time_ns(), message]
                self.add_value("mag", msg)
                ws.send(message)
        port = 5555
        print("Server running at: ", socket.gethostbyname(socket.gethostname())," port: ",port)
        self.setIP(socket.gethostbyname(socket.gethostname()))
        self.setPort(port)
        server = pywsgi.WSGIServer(('0.0.0.0', port), app, handler_class=WebSocketHandler)

        server.serve_forever()


if __name__ == '__main__':
    server= myServer(3)
    server.start()
    #thread_.start()
    #predictionThread.pred(server).start()

