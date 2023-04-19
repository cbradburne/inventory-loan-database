# Only use this if you're already using a booking system and need to import what's currently booked out

import csv
from tinydb import TinyDB
from tinydb.storages import JSONStorage
from datetime import datetime
import time

outDB = TinyDB('outdb.json')

with open('out.csv') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    line_count = 0
    for row in csv_reader:
        outDB.insert({'itemID': row[0], 
                        'userID': row[1], 
                        'longTerm': row[2], 
                        'dateID': (time.mktime(datetime.strptime(row[3], '%d/%m/%Y %H:%M').timetuple()))
                        })
        line_count += 1
    print(f'Processed {line_count} lines.')
