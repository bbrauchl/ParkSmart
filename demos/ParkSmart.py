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
ParkSmart_url = 'http://lamp.engin.umd.umich.edu/~bbrauchl/'
ParkSmart_url_local = 'http://localhost/ParkSmart/'

#Format for Image Inference data

# Call the web update API. At the time of writing, the web server
# will recieve the json, decode it, and respond with a string of
# from the php reconstruction of the sent object.
# get the docs: http://lamp.engin.umd.umich.edu/~bbrauchl/ParkSmart/api/update.html
def update_single(Lot : str, Space : int, IsOccupied : bool, Confidence : float = 0, Type : str = 'student', Extra=None, debug : bool = False):
    api_url = ParkSmart_url_local if (debug) else ParkSmart_url
    api_url += 'api/update.php'
    item = [{
        'Lot' : Lot,
        'Space' : Space,
        'IsOccupied' : IsOccupied,
        'Confidence' : Confidence,
        'Type' : Type,
        'Extra' : Extra if type(Extra) is str else '',
        }]
    return update_multi(states=item, debug=debug)

def update_multi(states : list, debug : bool = False):
    api_url = ParkSmart_url_local if (debug) else ParkSmart_url
    api_url += 'api/update.php'
    
    try: #check that the provided update is valid
        for state in states:
            assert (type(state) is dict), ("Error! each state within states array should be dict")
            # currenty will not be checked clientside
            # assert (type(state['Lot'] is str), ("Error! state['Lot'] should be provided as a string"))
            assert (type(state['Space']) is int), ("Error! state['Space'] should be provided as an int")
            assert (type(state['IsOccupied']) in [int, bool]), ("Error! state['IsOccupied'] should be bool")
            assert (type(state['Confidence']) is float), ("Error! state['Confidence' should be float")
            assert (type(state['Type']) is str and state['Type'] in ['student', 'faculty', 'visitor', 'handicap', 'electric_vehicle']), ("Error! state['Type'] should be one of the following strings: ['student', 'faculty', 'visitor', 'handicap', 'electric_vehicle']")
            if(type(state.get('Extra')) is not str):
                state['Extra'] = ''
    except KeyError as err:
        raise Exception("Error! key {} was not included in state".format(err))
    else:
        return requests.post(api_url, data={'payload':json.dumps(states)})
    

# Call the web pull API. This will pull the current occupancy states from the
# database and report them.
def pull(Lot : str, getIsOccupied : bool = True, getConfidence : bool = False, getType : bool = False, 
         getExtra : bool = False, getStartTimestamp : bool = False, getEndTimestamp : bool = False, debug : bool = False):
    api_url = ParkSmart_url_local if (debug) else ParkSmart_url
    api_url += 'api/pull.php'
    options = {
        'lot': Lot,
        'getIsOccupied':getIsOccupied,
        'getConfidence':getConfidence,
        'getType':getType,
        'getExtra':getExtra,
        'getStartTimestamp':getStartTimestamp,
        'getEndTimestamp':getEndTimestamp,
        }
    return requests.post(api_url, data=options)
    
# Call a sql query using the sql API. Pass in the required information for the
# server to access the database. for the server to access a database located
# on the same server, localhost must be used.
# This function will be removed in the actual release for security concerns
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

# calls the echo page. this will take a dict data and send it to the
# server, which sill echo its unpacking of the data
def echo(data, debug : bool = False):
    api_url = ParkSmart_url_local if (debug) else ParkSmart_url
    api_url += '/api/echo.php'
    #format data in an acceptable format
    if (type(data) is not dict):
        payload = {'payload' : json.dumps(data)}
    else:
        payload = { key : json.dumps(element) for key, element in data.items() }
        
    return requests.post(api_url, data=payload)
