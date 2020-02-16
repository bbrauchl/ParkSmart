# -*- coding: utf-8 -*-
"""
Created on Sat Feb 15 20:13:57 2020

@author: Bryan
"""

# this is used to create a simple interface to the server in python
# this will contain some functions to assist in these accesses.

import requests
import json

#base url for the project. Each api call will append its specific
#interface to the call.
ParkSmart_url = 'http://lamp.engin.umd.umich.edu/~bbrauchl/ParkSmart/'
ParkSmart_url_local = 'http://localhost/ParkSmart/'

# Call the web update API. At the time of writing, the web server
# will recieve the json, decode it, and respond with a string of
# from the php reconstruction of the sent object.
def update(item, debug : bool = False):
    api_url = ParkSmart_url_local if (debug) else ParkSmart_url
    api_url += 'api/update.php'
    r = requests.post(api_url, data={'json_payload':json.dumps(item)} )
    print(r.text)
    
# Call a sql query using the sql API. Pass in the required information for the
# server to access the database. for the server to access a database located
# on the same server, localhost must be used.
def sql(sql_query : str, sql_servername='localhost', sql_username='ParkSmart', sql_password=None, sql_database='parksmartdb', debug : bool = False):
    api_url = ParkSmart_url_local if (debug) else ParkSmart_url
    api_url += 'api/sql.php'
    #construct a payload in the format expected by the api
    payload = {
        'sql_query':sql_query,
        'sql_servername':sql_servername,
        'sql_username':sql_username,
        'sql_password':sql_password,
        'sql_database':sql_database}
    r = requests.post(api_url, data=payload);
    return r