import json
import os
import sys

PWD = os.path.dirname(os.path.realpath(__file__ ))
filepath = os.path.abspath(os.path.join(PWD, "..", ".."))
sys.path.append(filepath)
os.environ['DJANGO_SETTINGS_MODULE'] = 'Inebriator.settings'

from models import *

path = os.path.dirname(os.path.realpath(__file__))

with open('%s/../../drink_scraper/dofw_data.json' % path) as data_file:
    data = json.load(data_file)
drink_name = data['name']
drink = Drink(name=name)
drink.save()
