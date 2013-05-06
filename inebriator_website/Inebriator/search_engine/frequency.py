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

bad_unicode = [u'\xbe', u'\xbc', u'\xbd', u'\n']
already_used = {}
ingredient_triple = Ingredient.objects.all()
drinks = Drink.objects.all()

#doc_freq = {}
term_freq = {}
total = 0.0

for ingredient in ingredient_triple:
    terms = ingredient.name.split()
    for term in terms:
        term = term.lower()
        if term in term_freq:
            #doc_freq[term] = 1
            term_freq[term] = term_freq[term] +1
        else:
            term_freq[term] = 1.0

        total = total +1

for drink in drinks:
    terms = drink.name.split()
    for term in terms:
        term = term.lower()
        if term in term_freq:
            #doc_freq[term] = 1
            term_freq[term] = term_freq[term] +1
        else:
            term_freq[term] = 1.0

        total = total +1

term_sum = 0.0
with transaction.commit_on_success():
    for k,v in term_freq.items():
        term_sum += v/total
        term_object = Frequency(name=k, quantity=v/total)
        print k.encode('utf-8')
        print v/total
        term_object.save()

print term_sum


"""
counter = 0.0
total = 0.0
for ingredient in ingredient_triple:
    counter += 1.0
with transaction.commit_on_success():
    for ingredient in ingredient_triple:
        name_drink = ingredient.name
        if name_drink not in already_used:
            bad_flag = False
            for bad in bad_unicode:
                if bad in name_drink:
                    bad_flag = True
            if bad_flag == True:
                continue
            already_used[name_drink] = name_drink
            counter_sum = 0.0
            for ingredient_iter in ingredient_triple:
                name_iter = ingredient_iter.name
                if name_iter == name_drink:
                    counter_sum += 1.0
            frequency = counter_sum / counter
            total += frequency
            print name_drink.encode('utf-8')
            print frequency
            term = Frequency(name=name_drink.lower(), quantity=frequency)
            term.save()
print total
"""
