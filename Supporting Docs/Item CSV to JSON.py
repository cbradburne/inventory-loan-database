# Make sure that the CSV file is stored in the same directory as this file

import csv
from tinydb import TinyDB

itemDB = TinyDB('itemdb.json')

with open('items.csv') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    line_count = 0
    for row in csv_reader:
        itemDB.insert({'itemID': row[0],
                        'itemName': row[1], 
                        'itemMake': row[2], 
                        'itemModel': row[3], 
                        'itemSerial': row[4]})
        line_count += 1

    print(f'Processed {line_count} lines.')