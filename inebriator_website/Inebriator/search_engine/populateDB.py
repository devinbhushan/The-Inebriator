import json
import os
import sys
import ast

PWD = os.path.dirname(os.path.realpath(__file__))
filepath = os.path.abspath(os.path.join(PWD, "..", ".."))
sys.path.append(filepath)
os.environ['DJANGO_SETTINGS_MODULE'] = 'Inebriator.settings'

from models import *
from django.db import transaction
import csv

path = os.path.dirname(os.path.realpath(__file__))

csvfile = open('%s/../../../drink_scraper/Drinks_Mixer.csv' % path, 'rb')
data = csv.reader(csvfile)

header = True
with transaction.commit_on_success():
    for row in data:
        if header:
            header = False
            continue
        drink_list = ['drink_rating', 'drink_num_review', 'drink_name', 'drink_tags', 'drink_directions', 'drink_ingredients']
        num = 0
        for drink_item in drink_list:
            curr_value = 'row[num]'
            if curr_value is '':
                curr_value = None
            exec "%s = %s" % (drink_item, curr_value)
            num += 1
        if not drink_rating or drink_num_review is None:
            drink_rating = None
            drink_num_review = None
        if drink_directions is '' or drink_ingredients is '':
            continue
        drink = Drink(name=drink_name, rating=drink_rating, num_ratings=drink_num_review, directions=json.dumps(drink_directions))

        # Check for Duplicate drinks in database
        try:
            duplicate_drink = Drink.objects.get(name=drink_name)
            print "Drink already exists: %s" % drink_name
            continue
        except:
            drink.save()

        try:
            drink_ingredients = ast.literal_eval(drink_ingredients)
        except SyntaxError:
            pass
        for ingredient_tuple in drink_ingredients:
            ingredient_quantity, ingredient_name, ingredient_unit = ingredient_tuple
            ingredient = Ingredient(name=ingredient_name, unit=repr(ingredient_unit), amount=repr(ingredient_quantity))
            ingredient.save()
            drink.ingredients.add(ingredient)
            drink.save()
