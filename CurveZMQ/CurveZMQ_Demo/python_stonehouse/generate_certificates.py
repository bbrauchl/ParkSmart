#!/usr/bin/env python

#!pip install pyzmq

import zmq.auth
import sys
import os
import argparse
from shutil import rmtree

ap = argparse.ArgumentParser()
ap.add_argument("-d", "--delete", action="store_true", required=False, default=False,
    help="delete the current certificates in the .\.keys\ and .\.keys.secret\ directories")
args = vars(ap.parse_args())

# this simple if statement ensures that this file is being run 
# and is not being called from another python script
if __name__ == '__main__':
    
    # get relevant file system paths
    base_dir = os.path.dirname(__file__)
    local_dir = '.'
    server_name = 'server'
    client_name = 'client'

    public_key_dir = os.path.join(local_dir, '.keys')
    secret_key_dir = os.path.join(local_dir, '.keys.secret')
    
    # Delete Existing Certs if they exist
    if os.path.exists(public_key_dir):
        rmtree(public_key_dir)
    if os.path.exists(secret_key_dir):
        rmtree(secret_key_dir)

    if args["delete"] == False:
        public_server_file, secret_server_file = zmq.auth.create_certificates(local_dir, server_name)
        public_client_file, secret_client_file = zmq.auth.create_certificates(local_dir, client_name)

        public_server_file_target = os.path.join(public_key_dir, public_server_file).replace('\\.\\', '\\')
        secret_server_file_target = os.path.join(secret_key_dir, secret_server_file).replace('\\.\\', '\\')
        public_client_file_target = os.path.join(public_key_dir, public_client_file).replace('\\.\\', '\\')
        secret_client_file_target = os.path.join(secret_key_dir, secret_client_file).replace('\\.\\', '\\')

        if not os.path.exists(public_key_dir):
            os.mkdir(public_key_dir)
        if not os.path.exists(secret_key_dir):
            os.mkdir(secret_key_dir)

        os.rename(public_server_file, public_server_file_target)
        os.rename(secret_server_file, secret_server_file_target)
        os.rename(public_client_file, public_client_file_target)
        os.rename(secret_client_file, secret_client_file_target)
        
        print("Generated: "+str(public_server_file_target))
        print("Generated: "+str(public_client_file_target))
        print("Generated: "+str(secret_server_file_target))
        print("Generated: "+str(secret_client_file_target))

    else:
        print("Removed: "+str(public_key_dir))
        print("Removed: "+str(secret_key_dir))
