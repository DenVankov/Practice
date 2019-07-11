#!/usr/bin/env python
# -*- coding: utf-8 -*-

import socket
import socket
import random
from PIL import Image, ImageDraw

socket = socket.socket()
socket.connect(('localhost', 4040))


file = open("BP.jpg", "rb+")
data = file.read(1024)

while data:
    socket.send(data)
    data = file.read(1024)

file.close()
feedback = socket.recv(1024)
socket.close()
print feedback
