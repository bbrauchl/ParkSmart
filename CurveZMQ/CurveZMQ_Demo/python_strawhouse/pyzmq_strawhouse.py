#!/usr/bin/env python

# !pip install pyzmq

import sys
import os

import zmq
import zmq.auth
import zmq.auth.thread

# this simple if statement ensures that this file is being run
# and is not being called from another python script
if __name__ == '__main__':
    base_dir = os.path.dirname(__file__)

    zmq_context = zmq.Context.instance()

    # Set up the allow authenticator
    zmq_authenticator_allow = zmq.auth.thread.ThreadAuthenticator(context=zmq_context)
    zmq_authenticator_allow.start()
        
    # Put the ip we are listening to in the whitelist    
    zmq_authenticator_allow.allow('127.0.0.1')
     
    server_sock_allow = zmq_context.socket(zmq.PUSH)
    client_sock_allow = zmq_context.socket(zmq.PULL)

    # here we can specify specific IPs to listen for or specific hostnames
    # for now, only bind to localhost
    server_sock_allow.zap_domain = b'global' # must come before bind
    server_sock_allow.bind('tcp://127.0.0.1:9000')

    # have the client connect to localhost on the same port
    client_sock_allow.connect('tcp://127.0.0.1:9000')

    # test string to send over the socket
    test_string_allow = "Strawhouse Pattern Test String Allow"

    # try sending the test string
    server_sock_allow.send(bytes(test_string_allow, 'utf-8'))

    recieved_test_string_allow = client_sock_allow.recv().decode('utf-8')

    server_sock_allow.close()
    client_sock_allow.close()
    
    zmq_authenticator_allow.stop()

    # Set up deny authenticator
    zmq_authenticator_deny = zmq.auth.thread.ThreadAuthenticator(context=zmq_context)
    zmq_authenticator_deny.start()

    # Put the ip we are listening to in the blacklist 
    zmq_authenticator_deny.deny("127.0.0.1")

    server_sock_deny = zmq_context.socket(zmq.PUSH)     
    client_sock_deny = zmq_context.socket(zmq.PULL)

    # here we can specify specific IPs to listen for or specific hostnames
    # for now, only bind to localhost
    server_sock_deny.zap_domain = b'global' # must come before bind
    server_sock_deny.bind("tcp://127.0.0.1:9000")

    # have the client connect to localhost on the same port
    client_sock_deny.connect("tcp://127.0.0.1:9000")

    # test string to send over the socket
    test_string_deny = "Strawhouse Pattern Test String Deny"

    if server_sock_deny.poll(50, zmq.POLLOUT):
        server_sock_deny.send(bytes(test_string_deny, 'utf-8'))

        if client_sock_deny.poll(50):
            recieved_test_string_deny = client_sock_deny.recv().decode('utf-8')
        else:
            recieved_test_string_deny = ""
    else:
        recieved_test_string_deny = ""
    
    server_sock_deny.close()
    client_sock_deny.close()
    
    print("Python ZMQ Strawhouse Pattern (Whitelisted)")
    print("Sent (allow): \""+test_string_allow+"\"")
    print("Recv (allow): \""+recieved_test_string_allow+"\"")
    print("Sent (deny): \""+test_string_deny+"\"")
    print("Recv (deny): \""+recieved_test_string_deny+"\"")
    
    if test_string_allow == recieved_test_string_allow and test_string_deny != recieved_test_string_deny:
        print("Strawhouse Test OK")
    else:
        print("Strawhouse Test Failed")
