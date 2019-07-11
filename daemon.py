#!/usr/bin/env python
# -*- coding: utf-8 -*-

import socket
import numpy as np
import cv2
import sys
import os
import base64
from PIL import Image

class Daemon:

    def __init__(self):
        self.socket = socket.socket()
        self.socket.bind(('', 4040))
        self.socket.listen(100)
        log.write("Server was initiated\n")

    def start(self, file):
        while True:
            self.connection, self.address = self.socket.accept()
            print 'connected to: ', self.connection, self.address
            log.write("Connection complete\n")
            self.file = open(file, 'wb+')
            while True:
                data = self.connection.recv(1024)
                if not data:
                    break
                self.file.write(data)
                data = self.connection.recv(1024)
                string = "File was recieved and saved\n"
                log.write(string)
                self.connection.send(string)
                while data:
                    self.file.write(data)
                    data = self.connection.recv(1024)
            self.file.close()
            log.write("Starting recognizing\n")
            face_recognize(file)
            log.write("Regognition complete\n")
            self.connection.close()


def face_recognize(file):
    recognizer = cv2.face.createLBPHFaceRecognizer()
    recognizer.load('trainer/trainer.yml')

    log.write("Trainer was loaded\n")
    cascade_path = "haarcascade_frontalface_default.xml"
    face_cascade = cv2.CascadeClassifier(cascade_path)

    font = cv2.FONT_HERSHEY_SIMPLEX

    id = 0 # id counter

    names = ['No one', 'Denis', 'Danila', 'Artem', 'Brad Pitt']

    while True:
        input = cv2.imread(file, 1)
        img = cv2.resize(input, None, fx=0.5, fy=0.5, interpolation = cv2.INTER_CUBIC)
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, scaleFactor = 1.2, minNeighbors = 5, minSize = (20, 20))

        for (x, y, w, h) in faces:
            cv2.rectangle(img, (x,y), (x + w, y + h), (255, 0, 0), 2)
            id, confidence = recognizer.predict(gray[y: y + h, x: x + w])

            if (confidence < 100):
                id = names[id]
                confidence = " {0}%".format(round(100 - confidence))
            else:
                id = "unknown"
                confidence = " {0}%".format(round(100 - confidence))

            cv2.putText(img, str(id), (x + 5, y - 5), font, 1, (255, 255, 255), 2)
            cv2.putText(img, str(confidence), (x + 5, y + h - 5), font, 1, (255, 255, 0), 1)
            cv2.imshow('Recognized image', img)
            cv2.imwrite(os.path.join('./', 'rec.jpg'), img)

        k = cv2.waitKey(15) & 0xFF
        if k == 27:
            break
    log.write("Image was recognized and saved with frame\n")
    cv2.destroyAllWindows()

log = open('logging.txt', 'wb+')
server = Daemon()
file = 'new_file.jpg'
server.start(file)
log.write("Server was switched off\n")
log.close()
