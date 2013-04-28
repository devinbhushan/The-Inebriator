import json
import os
import sys
import ast

PWD = os.path.dirname(os.path.realpath('__file__'))
filepath = os.path.abspath(os.path.join(PWD, "..", ".."))
sys.path.append(filepath)
os.environ['DJANGO_SETTINGS_MODULE'] = 'Inebriator.settings'

from models import *
import csv

already_used = []
ingredient_triple = Ingredient.objects.all()
counter = 0
for ingredient in ingredient_triple:
    counter += 1
for ingredient in ingredient_triple:
    name_drink = ingredient.name
    if name_drink not in already_used:
        already_used.append(name)
        counter_sum = -1
        for ingredient_iter in ingredient_triple:
            name_iter = ingredient_iter.name
            if name_iter == name_drink:
                counter_sum += 1
        frequency = counter_sum / counter
        print name
        print frequency
        term = Frequency(name=name_drink, quantity=frequency)
        term.save()