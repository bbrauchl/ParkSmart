
import requests
import json
import ParkSmart
import random

test_object = { #create an object to get sent to the server
        'name' : 'Ronald McDonald',
        'favorite_food' : 'americans',
        'dumb_array' : [ 1, ['hello'], [], [[['hi'], 42069], [False], True], 42 ],
        'dictionary' : { 'a' : 'apples', 'b':'bananas', 'c':'cherries', 'd': ';)' },
        'data' : [random.random() for i in range(10)]
    }


ParkSmart.update(test_object, debug=True)

resp = ParkSmart.sql("SELECT * FROM Lot_D;", debug=True).json()

for space in resp:
    print('space {} is {} with a confidence of {}'.format(space['Space'], 'occupied' if int(space['IsOccupied']) else 'vacent', space['Confidence']))