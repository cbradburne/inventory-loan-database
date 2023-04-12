# Make sure that the CSV file is stored in the same directory as this file

import csv
from tinydb import TinyDB

userDB = TinyDB('userdb.json')

with open('users.csv') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    line_count = 0
    for row in csv_reader:
        userDB.insert({'userID': row[0],
                        'firstName': row[1], 
                        'lastName': row[2], 
                        'email': row[3]})
        line_count += 1

    print(f'Processed {line_count} lines.')