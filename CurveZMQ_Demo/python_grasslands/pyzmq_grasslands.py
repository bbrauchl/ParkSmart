#!/usr/bin/env python

# !pip install pyzmq

import sys
import os

import zmq
import zmq.auth
from zmq.auth.thread import ThreadAuthenticator

# this simple if statement ensures that this file is being run
# and is not being called from another python script
if __name__ == '__main__':
    base_dir = os.path.dirname(__file__)

    zmq_context = zmq.Context()

    server_sock = zmq_context.socket(zmq.PUSH)
    client_sock = zmq_context.socket(zmq.PULL)

    # here we can specify specific IPs to listen for or specific hostnames
    # for now, only bind to localhost
    server_sock.bind("tcp://127.0.0.1:9000")

    # have the client connect to localhost on the same port
    client_sock.connect("tcp://127.0.0.1:9000")

    # test string to send over the socket
    test_string = "Grassland Pattern Test String"

    # try sending the test string
    server_sock.send(bytes(test_string, 'ascii'))

    recieved_test_string = client_sock.recv().decode('ascii')
    
    print("Python ZMQ Grassland Pattern")
    print("Sent: \""+test_string+"\"")
    print("Recv: \""+recieved_test_string+"\"")
    
    if test_string == recieved_test_string:
        print("Grasslands Test OK")
    else:
        print("Grasslands Test Failed")
