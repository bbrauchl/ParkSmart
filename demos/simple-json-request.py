
import requests
import json
import ParkSmart
import random


#test of update API
print('Test of update API')
print('Updating space 0')
for i in range(85):
    resp = ParkSmart.update(Lot='Lot_D', Space=i, IsOccupied=True if random.randint(0,1) else False, Confidence=random.random(), Type='student' if not i in range(73, 80) else 'handicap', debug=False)

print(resp.text)

# test of sql call API
print("")
print('Test of SQL API')
print('Calling SQL to select all of table \'Lot_D\'')
# get the current state of the database
try:
    current_database = ParkSmart.sql('SELECT * FROM Lot_D', debug=False).json()
except:
    print('error, could not extract server response as JSON')
else:
    print('Success!')

print("")  
print('printing{} contents of received object:'.format(" some of" if len(current_database) > 6 else ""))
# get the current state of Parking space 0 (the one that was updated above)
if len(current_database) > 6:
    print(current_database[:3])
    print("...")
    print(current_database[-3:])
else:
    print(current_database)

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

