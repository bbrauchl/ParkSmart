# -*- coding: utf-8 -*-
"""
This is a demonstration on how to use the Parksmart update API in python.

I have created a file that can be imported as a module to aid in calling server APIs

"""

# Main import, needed to use this library to make calls to the server
import ParkSmart

from random import *



#### 1. Using the Update-single API to perform an update of a single parking space:

# string corrisponding to the database name of the lot
Lot = 'Lot_D' 
# Integer number corrisponding to the space ID.
Space = randint(0, 83)
# bool that is true when the associated space is occupied
IsOccupied = True if randint(0,1) else False 
# float between 0 and 1 representing how confident the model is in the prediction
Confidence = random() 
# String representing the type of parking spot. Possible values: ['student', 'faculty', 'visitor', 'handicap', 'electric_vehicle']
Type = ['student', 'faculty', 'visitor', 'handicap', 'electric_vehicle'][randint(0,4)]
# optionial String representing any extra data to be attached to the parking space
Extra = "I am a parking space"

resp = ParkSmart.update_single(Lot=Lot, Space=Space, IsOccupied=IsOccupied, Confidence=Confidence, Type=Type, Extra=Extra)
# Resp is a http Response object, so use .text to get the text body of the response
print(resp.text)
#you can also call without the Extra Parameter 
resp = ParkSmart.update_single(Lot=Lot, Space=Space, IsOccupied=IsOccupied, Confidence=Confidence, Type=Type)
# Resp is a http Response object, so use .text to get the text body of the response
print(resp.text)


#### 2. (Reccomended Method) Using the Update-multi API

# The update information provided above must be stored in a dictionary as follows. Case is important!!
# notice that this is a list of dictionaries. Even if there is only one spot in the update it needs
# to be in the list format!!
update_item = [
    {
     'Lot' : 'Lot_D',
     'Space': 12,
     'IsOccupied': True,
     'Confidence': 0.01,
     'Type': 'student',
     'Extra': "I am spaec 12!"
    },
    {
     'Lot' : 'Lot_D',
     'Space': 14,
     'IsOccupied': False,
     'Confidence': 0.99,
     'Type': 'visitor',
     #No extra information
    }
]

# call to push to the server
ParkSmart.update_multi(update_item)

# this can also be done with a list comprehension to make it much prettier
# randomly update spaces 30-69
update_item = [
    {
     'Lot': 'Lot_D',
     'Space': i,
     'IsOccupied': True if randint(0,1) == 1 else False,
     'Confidence': random(),
     'Type': 'electric_vehicle' if i in range(0,4) else 'handicap' if i in range(73, 80) else 'student',
     } for i in range(30,70)]
ParkSmart.update_multi(update_item)


