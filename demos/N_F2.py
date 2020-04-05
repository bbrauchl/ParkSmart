# -*- coding: utf-8 -*-
"""
Created on Sun Apr  5 02:46:52 2020

@author: Bryan
"""

import ParkSmart
import requests
from random import *
import time
import math

#testing database commit and retrieval
print("----------Start Consistency test-------------")
trials = 10
for i in range(trials):
    # push a randomly generated update
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
    
    #consistancy check:
    data = ParkSmart.pull(Lot="Lot_D").json()
    #reformat response for easier comparison
    data = [{ 'Lot': 'Lot_D',
             'Space': int(ele['Space']),
             'IsOccupied': True if ele['IsOccupied'] == '1' else False,
             'Confidence': float(ele['Confidence']),
             'Type': ele['Type']} for ele in data['Lot_D']]
    update_item.sort(key = lambda x: x['Space'])
    data.sort(key = lambda x: x['Space'])
    
    err_cnt = abs(len(update_item) - len(data))
    for org, rec in zip(update_item, data):
        try:
            for org_item, rec_item in zip(org, rec):
                if org_item == rec_item:
                    continue
                raise RuntimeError("recieved {} does not match {}".format(rec_item, org_item))
                
        except RuntimeError as error:
            print("Eror!!:", error)
            err_cnt += 1

print("Corrilation rate: {}%".format(100*(1-err_cnt/(10*len(update_item)))), end='')
print(" {}, ({}/{})".format("PASS" if err_cnt < (trials*len(update_item))/100 else "FAIL", (trials*len(update_item))-err_cnt,(trials*len(update_item))  ))
print("----------End Consistency test-------------")

print("----------Start Access test-------------")
#the device should be consistently accessable. Drops in access could be detramental to the system
#this test will test the access to the server over a period of time

trial_length = 4 * 60 * 60 * 60 # 12 hour test (in seconds)
trial_period = 60 # each access will be 1 minuite apart.
err_cnt = 0
success_cnt = 0
trials = trial_length/trial_period
for i in range(math.ceil(trials)):
    time.sleep(trial_period)
    try:
        resp = requests.get("http://lamp.engin.umd.umich.edu/~bbrauchl/build/index.html")
    except requests.HTTPError as err:
        print ("Encountered HTTP error: {} (trial {})".format(err,i))
        err_cnt += 1
    except Exception as err:
        print ("Encountered Exception: {} (trial {})".format(err,i))
        err_cnt += 1
    else:
        success_cnt += 1
        # print success message every 1000 trials
        if (i % 1000 == 0):
            print ("Trial {} successful".format(i))

print("Total Errors: {}".format(err_cnt))
print("Accessablility: {}%".format(success_cnt/trials))
print("----------End Access test-------------")