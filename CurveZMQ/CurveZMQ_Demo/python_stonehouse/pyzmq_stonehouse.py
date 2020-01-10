#!/usr/bin/env python

# !pip install pyzmq

import sys
import os
import argparse
import logging
import time

import zmq
import zmq.auth
import zmq.auth.thread

ap = argparse.ArgumentParser()
ap.add_argument("-s", "--server", required=False, default='127.0.0.1',
    help="Provide an IP to connect to. if none supplied \"127.0.0.1\" will be used")
ap.add_argument("-p", "--port", required=False, default='5555',
    help="Provide an IP to connect to. if none supplied \"5555\" will be used")
ap.add_argument("-u", "--udp", action="store_true", required=False, default=False,
    help="use udp protocol")
args = vars(ap.parse_args())

connection_ip = args.get("server", "127.0.0.1")
connection_port = args.get("port", "5555")
connection_protocol = "udp" if args.get("udp") == True else "tcp"
print("Connection: {}://{}:{}".format(connection_protocol, connection_ip, connection_port))

stonehouse_test_string_allow = "Stonehouse Pattern Test String Allow"
stonehouse_test_string_deny = "Stonehouse Pattern Test String Deny"


# this simple if statement ensures that this file is being run
# and is not being called from another python script
if __name__ == '__main__':
    base_dir = os.path.dirname(__file__)

    public_keys_dir = os.path.join(base_dir, '.keys')
    secret_keys_dir = os.path.join(base_dir, '.keys.secret')

    if not (os.path.exists(public_keys_dir) and
            os.path.exists(secret_keys_dir)):
        logging.critical("Certificates are missing: run generate_certificates.py script first")
        sys.exit(1)

    zmq_context = zmq.Context.instance()

    # Set up the allow authenticator
    zmq_authenticator_allow = zmq.auth.thread.ThreadAuthenticator(context=zmq_context)
    zmq_authenticator_allow.start()
        
    # Put the ip we are listening to in the whitelist    
    zmq_authenticator_allow.allow(connection_ip)
    # Tell the authenticator how to handle CURVE requests
    zmq_authenticator_allow.configure_curve(domain='*', location=zmq.auth.CURVE_ALLOW_ANY)
    
    # set up CURVE encryption on the server socket.
    server_sock_allow = zmq_context.socket(zmq.PUSH)
    server_secret_file = os.path.join(secret_keys_dir, "server.key_secret")
    server_public, server_secret = zmq.auth.load_certificate(server_secret_file)
    server_sock_allow.curve_secretkey = server_secret
    server_sock_allow.curve_publickey = server_public

    # set up CURVE encryption on the client socket.
    client_sock_allow = zmq_context.socket(zmq.PULL)
    client_secret_file = os.path.join(secret_keys_dir, "client.key_secret")
    client_public, client_secret = zmq.auth.load_certificate(client_secret_file)
    client_sock_allow.curve_secretkey = client_secret
    client_sock_allow.curve_publickey = client_public

    # now the client must also know the server's public key.
    server_public_file = os.path.join(public_keys_dir, "server.key")
    server_public, _ = zmq.auth.load_certificate(server_public_file)
    client_sock_allow.curve_serverkey = server_public

    # connect
    server_sock_allow.curve_server = True
    server_sock_allow.bind("{}://*:{}".format(connection_protocol, connection_port))

    client_sock_allow.connect("{}://{}:{}".format(connection_protocol, connection_ip, connection_port))

    #try sending over the socket (this should be successful)
    if server_sock_allow.poll(50, zmq.POLLOUT):
        server_sock_allow.send(bytes(stonehouse_test_string_allow, 'utf-8'))

        if client_sock_allow.poll(50):
            recieved_test_string_allow = client_sock_allow.recv().decode('utf-8')
        else:
            recieved_test_string_allow = ""
    else:
        recieved_test_string_allow = ""
    
    #close the sockets and authenticator.
    server_sock_allow.close()
    client_sock_allow.close()
    zmq_authenticator_allow.stop()


    # Set up the deny authenticator
    zmq_authenticator_deny = zmq.auth.thread.ThreadAuthenticator(context=zmq_context)
    zmq_authenticator_deny.start()
        
    # Put the ip we are listening to in the whitelist    
    zmq_authenticator_deny.allow(connection_ip)
    # Tell the authenticator how to handle CURVE requests
    zmq_authenticator_deny.configure_curve(domain='*', location=zmq.auth.CURVE_ALLOW_ANY)
    
    # set up CURVE encryption on the server socket.
    server_sock_deny = zmq_context.socket(zmq.PUSH)
    server_secret_file = os.path.join(secret_keys_dir, "server.key_secret")
    server_public, server_secret = zmq.auth.load_certificate(server_secret_file)
    
    # here is where the magic happens, lets say that a mallicious server doesnt have the private key
    server_sock_deny.curve_secretkey = server_public
    server_sock_deny.curve_publickey = server_public

    # set up CURVE encryption on the client socket.
    client_sock_deny = zmq_context.socket(zmq.PULL)
    client_secret_file = os.path.join(secret_keys_dir, "client.key_secret")
    client_public, client_secret = zmq.auth.load_certificate(client_secret_file)
    client_sock_deny.curve_secretkey = client_secret
    client_sock_deny.curve_publickey = client_public

    # now the client must also know the server's public key.
    server_public_file = os.path.join(public_keys_dir, "server.key")
    server_public, _ = zmq.auth.load_certificate(server_public_file)
    client_sock_deny.curve_serverkey = server_public

    # connect
    server_sock_deny.curve_server = True
    server_sock_deny.bind("{}://*:{}".format(connection_protocol, connection_port))

    client_sock_deny.connect("{}://{}:{}".format(connection_protocol, connection_ip, connection_port))

    #try sending over the socket (this should be successful)
    if server_sock_deny.poll(50, zmq.POLLOUT):
        server_sock_deny.send(bytes(stonehouse_test_string_deny, 'utf-8'))

        if client_sock_deny.poll(50):
            recieved_test_string_deny = client_sock_deny.recv().decode('utf-8')
        else:
            recieved_test_string_deny = ""
    else:
        recieved_test_string_deny = ""
    
    #close the sockets and authenticator.
    server_sock_deny.close()
    client_sock_deny.close()
    zmq_authenticator_deny.stop()

    print("Python ZMQ Strawhouse Pattern (Encrypted)")
    print("Sent (allow): \""+stonehouse_test_string_allow+"\"")
    print("Recv (allow): \""+recieved_test_string_allow+"\"")
    print("Sent (deny): \""+stonehouse_test_string_deny+"\"")
    print("Recv (deny): \""+recieved_test_string_deny+"\"")

    if stonehouse_test_string_allow == recieved_test_string_allow and stonehouse_test_string_deny != recieved_test_string_deny:
        print("Stonehouse Test OK")
    else:
        print("Stonehouse Test Failed")