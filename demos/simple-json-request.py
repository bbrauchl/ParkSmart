
import requests
import json
import ParkSmart
import random


#test of update API
print('Test of update API')
print('Updating space 0')
resp = ParkSmart.update(Lot='lot_d', Space=0, IsOccupied=True, Confidence=random.random(), Type='student', debug=True)
print(resp.text)

# test of sql call API
print("")
print('Test of SQL API')
print('Calling SQL to select all of table \'lot_d\'')
# get the current state of the database
try:
    current_database = ParkSmart.sql('SELECT * FROM Lot_D', debug=True).json()
except:
    print('error, could not extract server response as JSON')
else:
    print('Success!')
print('printing contents of space 0 recieved object:')
# get the current state of Parking space 0 (the one that was updated above)
print(current_database[0])

#test of the echo api
print("")
print('Test of echo API')
test_object = {
    'array_item' : [1, 'two', 3.0],
    'string_item' : "hello world",
    'integer_item': 12,
    'dictionary_item' : {'one' : 1, 'two' : 2, 'array':[1,2,3,4,'hello']}
    }
resp = ParkSmart.echo(test_object, debug=True)
print(resp.text)
