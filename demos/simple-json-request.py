
import requests
import json
import ParkSmart
import random
import time
import sys
import os
import numpy as np


#test of update_single API
print('Test of update_single API')
print('Updating space 0')

resp = ParkSmart.update_single(Lot='Lot_D', Space=0, IsOccupied=True if random.randint(0,1) else False, Confidence=random.random(), Type='electric_vehicle', debug=False)
print(resp.text)


#test of update_multi API
print('Test of update_multi API')
print('Updating space 1-83')
multi_update_states = [{
        'Lot' : 'Lot_D',
        'Space' : Space,
        'IsOccupied' : True if random.randint(0,1) else False,
        'Confidence' : random.random(),
        'Type' : 'electric_vehicle' if Space in range(0,4) else 'handicap' if Space in range(73, 80) else 'student',
        } for Space in range(1,84)]
resp = ParkSmart.update_multi(states=multi_update_states, debug=False)
print(resp.text)


#test of the echo api
print("")
print('Test of echo API')
test_object = {
    'array_item' : [1, 'two', 3.0],
    'string_item' : "hello world",
    'integer_item': 12,
    'dictionary_item' : {'one' : 1, 'two' : 2, 'array':[1,2,3,4,'hello']}
    }
resp = ParkSmart.echo(test_object, debug=False)
print(resp.text)

try:
    while True:
        #update randomly between 0 and 2 minuites
        time.sleep(random.randint(1,15))
        #update states to see changing in webserver
        multi_update_states = [{
        'Lot' : 'Lot_D',
        'Space' : Space,
        'IsOccupied' : True if random.randint(0,1) else False,
        'Confidence' : random.random(),
        'Type' : 'electric_vehicle' if Space in range(0,4) else 'handicap' if Space in range(73, 80) else 'student',
        } for Space in range(0, 84)]
        resp = ParkSmart.update_multi(states=multi_update_states, debug=False)
        print(resp.text)
except KeyboardInterrupt:
    print('Interrupted')