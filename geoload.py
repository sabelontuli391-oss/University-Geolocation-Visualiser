# -*- coding: utf-8 -*-
"""
Created on Thu Aug 21 18:04:23 2025

@author: sabel
"""

import json
import ssl
import sys
import sqlite3
import urllib.request, urllib.parse, urllib.error
import http
import time

serviceurl = 'https://py4e-data.dr-chuck.net/opengeo?'

#Additional detail for urllib
#http.client.HTTPConnection.debuglevel = 1

conn = sqlite3.connect('opengeo.sqlite')
cur = conn.cursor()

cur.execute("CREATE TABLE IF NOT EXISTS locations (address TEXT, geodata TEXT)")

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

fh = open('C:/Users/sabel/Downloads/opengeo/opengeo/where.data')
count = 0
nofound = 0
for line in fh:
    if count > 100:
        print('Retrieved 100 locations. Please restart to retrieve more.')
        break
    
    address = line.strip()
    print('')
    cur.execute("SELECT geodata FROM locations WHERE address = ?", (address,))
    
    try:
        data = cur.fetchone()[0]
        print("Found in database", address)
        continue
    except:
        pass
    
    parms = dict()
    parms['q'] = address
    url = serviceurl + urllib.parse.urlencode(parms)
    
    print("Retrieving", url)
    uh = urllib.request.urlopen(url, context=ctx)
    data = uh.read().decode()
    print('Retrived', len(data), 'characters', data[:20].replace('\n', ' '))
    count = count + 1
    
    try:
        js = json.loads(data)
    except:
        print(data) #We print in case unicode cuases an error
        continue
        
    if not js or 'features' not in js:
        print('==== Download eror ===')
        print(data)
        break
    
    if len(js['features']) == 0:
        print(' ==== Object not found ====')
        nofound = nofound + 1
        
    cur.execute(""" INSERT INTO locations (address, geodata) VALUES (?, ?)""",
    (memoryview(address.encode()), memoryview(data.encode())))
    
    conn.commit()
    
    if count % 10 == 0:
        print('Pausing for a bit...')
        time.sleep(5)
conn.close()       
if nofound > 0:
    print('Number of features for which the location could not be found:', nofound)
    
print("Run geodump.py to read the data from the database so you can visualise it on a map")
    
    
    
    
    
    
    