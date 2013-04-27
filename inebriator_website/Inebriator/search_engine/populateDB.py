import json
from models.Drink import Drink
import os

path = os.path.dirname(os.path.realpath(__file__))

with open('%s/../../drink_scraper/dofw_data.json' % path) as data_file:
    data = json.load(data_file)
drink_name = data['name']
drink = Drink(name=name)
drink.save()
