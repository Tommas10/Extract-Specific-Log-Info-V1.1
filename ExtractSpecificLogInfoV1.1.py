#!/usr/bin/env python

#Small automation Python script- Extract specific log information.
#Count occurrences of keywords, get the timestamp for specific occurrences of keywords, get the elapsed time of specific log entries
#Created by Tommas Huang 
#Created date: 2020-05-05

import numpy as np
import pandas as pd 
from datetime import datetime, timedelta

keywords = ['Moving patched file', 'Patching']
actions = ['WRITE(']
kws_dict = {}
acts_dict = {}

with open('/Users/tommashunag/Desktop/log/install.log') as l:
    with open('filtered.log', 'w') as f:
        for line in l:
            if any(k in line for k in keywords) and len(line) > 1:
                entry = line.split('-')[1].strip()
                dt = line.split('-')[0].strip()
                if entry in kws_dict:
                    kws_dict[entry].append(datetime.strptime(dt, '%Y-%m-%dT%H:%M:%S.%f'))
                else:
                    kws_dict[entry] = [datetime.strptime(dt, '%Y-%m-%dT%H:%M:%S.%f')]
            elif any(a in line for a in actions) and len(line) > 1:
                dt = line.split('-')[0].strip()
                action = line.split(' ')[-2].strip()
                action_type = line.split(' ')[-1].strip()
                if action in acts_dict.keys():
                    acts_dict[action][action_type] = datetime.strptime(dt,'%Y-%m-%dT%H:%M:%S.%f')
                else:
                    acts_dict[action] = {action_type:datetime.strptime(dt,'%Y-%m-%dT%H:%M:%S.%f')}

# print results
for k in kws_dict.keys():
    print('%s occured %s times' % (k, len(kws_dict[k])))
# comment below if you don't need specific timestamps
    for i in kws_dict[k]:
        print('\t%s' % i.strftime('%Y-%m-%dT%H:%M:%S.%f'))

#iterate over actions, then action_types (start, end)
for a, at in acts_dict.iteritems():
    print('%s: Elapsed time %s' % (a, at['end'] - at['start']))
#    for at, t in acts_dict[a].iteritems():
#        print('\t%s: %s' % (at, t.strftime('%Y-%m-%dT%H:%M:%S.%f')))

## Raw data in case you need it
#print("Actions:\n", acts_dict)