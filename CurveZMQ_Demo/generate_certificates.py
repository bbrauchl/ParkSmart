#!/usr/bin/env python

#!pip install pyzmq

import zmq.auth
import sys
import os


# this simple if statement ensures that this file is being run 
# and is not being called from another python script
if __name__ == '__main__':
    
    server_dir = '.'
    server_name = 'pyzmq_server'

    client_dir = '.'
    client_name = 'pyzmq_client'

    public_server_file, secret_server_file = zmq.auth.create_certificates(server_dir, server_name)
    public_client_file, secret_client_file = zmq.auth.create_certificates(client_dir, client_name)
   
    if len(sys.argv) > 1 and sys.argv[1] == '--delete':
        
        #if there is the delete keyword, remove the keys
        os.remove(public_server_file)
        os.remove(secret_server_file)
        os.remove(public_client_file)
        os.remove(secret_client_file)
        print("Removed: "+str(public_server_file)+", "+str(secret_server_file))
        print("Removed: "+str(public_client_file)+", "+str(secret_client_file))
    
    else:
        print("Generated: "+str(public_server_file)+", "+str(secret_server_file))
        print("Generated: "+str(public_client_file)+", "+str(secret_client_file))
