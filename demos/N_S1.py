# -*- coding: utf-8 -*-
"""
Created on Sun Apr  5 02:46:34 2020

@author: Bryan
"""

import ParkSmart
import requests
import json
from random import *
import time

print("----------Start Dropout Timing test-------------")
#creation of random test data
update_item = [
    {
     'Lot': 'Lot_D',
     'Space': i,
     'IsOccupied': True if randint(0,1) == 1 else False,
     'Confidence': random(),
     'Type': 'electric_vehicle' if i in range(0,4) else 'handicap' if i in range(73, 80) else 'student',
     } for i in range(0,85)]

print("Pushing test data")
ParkSmart.update_multi(update_item)

start_time = time.time()
print("Starting Timing. Current Time: {:.3f}".format(start_time))

#consistancy check:
data = ParkSmart.pull(Lot="Lot_D").json()
#reformat response for easy comparison
data = [{ 'Lot': 'Lot_D',
         'Space': int(ele['Space']),
         'IsOccupied': True if ele['IsOccupied'] == '1' else False,
         'Confidence': float(ele['Confidence']),
         'Type': ele['Type']} for ele in data['Lot_D']]

#poll the server using the pull function to see when it no longer reports the previous update
while True:
    data = ParkSmart.pull(Lot="Lot_D").json()
    if data.get("Lot_D", []) == [] or data.get("Lot_D", []) == None:
        break
    time.sleep(0.5) #sleep 0.5 second, measurements need not be more accurate than that.
    
end_time = time.time()
print("Data Expired! Current Time: {:.3f}".format(start_time))

print("Dropout Recognition Delay: {:.2f}s".format(end_time-start_time), end='')
print(" {}".format("EXCELENT" if end_time-start_time < 180 else "GOOD" if end_time-start_time < 300 else "FAIL" ))
print("----------End Dropout Timing test-------------")

print("----------Start API ERROR test-------------")

#tests the responses from calling the API with inproper payloads
#types are also checked by the python API, so raw requests need to be done to test this
test_Lot = ['Lot_D', 'Lot D', 'LOT_D', '', 2, [], True]
test_Space = [1, 1.0, '1', 'one', 'first', '', [], True]
test_IsOccupied = [True, 1, 1.0, '1', 'one', 'first', '', []]
test_Confidence = [0.5, "50%", '0.5', 'half', None, '', []]
test_Type = ['student', 'visitor', 'Student', 'FaCuLtY', None, 12, '', []]
test_Extra = ["hello", 123123, [], True, '']
                
print("testing the pull api")
for Lot in test_Lot:
    resp = requests.post("http://lamp.engin.umd.umich.edu/~bbrauchl/api/pull.php", data={'Lot':Lot})
    print("response to {}: {}".format(Lot, resp.text))

print("testing the update api")

for Lot in test_Lot:
    for Space in test_Space:
        for IsOccupied in test_IsOccupied:
            for Confidence in test_Confidence:
                for Type in test_Type:
                    for Extra in test_Extra:
                        item = [{
                                'Lot' : Lot,
                                'Space' : Space,
                                'IsOccupied' : IsOccupied,
                                'Confidence' : Confidence,
                                'Type' : Type,
                                'Extra' : Extra if type(Extra) is str else '',
                                }]
                        resp = requests.post("http://lamp.engin.umd.umich.edu/~bbrauchl/api/update.php", data={'payload':json.dumps(item)})
                        print("response to {}: {}".format(item[0], resp.text))

print("----------End API ERROR test-------------")