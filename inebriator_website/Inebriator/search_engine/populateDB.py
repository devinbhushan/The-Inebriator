import json
import os
import sys

PWD = os.path.dirname(os.path.realpath(__file__ ))
filepath = os.path.abspath(os.path.join(PWD, "..", ".."))
sys.path.append(filepath)
os.environ['DJANGO_SETTINGS_MODULE'] = 'Inebriator.settings'

from models import *
import csv

path = os.path.dirname(os.path.realpath(__file__))

csvfile = open('%s/../../../drink_scraper/dofw.csv' % path, 'rb')
data = csv.reader(csvfile)

i = 0
for row in data:
    if i is 0:
        i += 1
        continue
    print row
    drink_name = row[2]
    drink = Drink(name=drink_name)
    drink.save()
