import os
import sys
import ast

PWD = os.path.dirname(os.path.realpath(__file__))
filepath = os.path.abspath(os.path.join(PWD, "..", ".."))
sys.path.append(filepath)
os.environ['DJANGO_SETTINGS_MODULE'] = 'Inebriator.settings'

from models import *
import csv

print "setting up file output..."

path = os.path.dirname(os.path.realpath(__file__))
txtfile = open("%s/dictionary.txt" % path, 'wb')

ingreds = Ingredient.objects.all()
drinks = Drink.objects.all()

print "writing ingredients..."

for ingredient in ingreds:
    txtfile.write("%s " % repr(ingredient.name))

print "writing drinks..."

for drink in drinks:
    txtfile.write("%s " % repr(drink.name))

print "dictionary written"

txtfile.close()
