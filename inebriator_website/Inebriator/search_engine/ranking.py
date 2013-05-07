import os
import sys
import ast
from math import log
from Queue import PriorityQueue
import operator
from django.core.exceptions import ObjectDoesNotExist

PWD = os.path.dirname(os.path.realpath(__file__))
filepath = os.path.abspath(os.path.join(PWD, "..", ".."))
sys.path.append(filepath)
os.environ['DJANGO_SETTINGS_MODULE'] = 'Inebriator.settings'

from models import *

def rank(query_terms, drinks):

    #Split all the query terms by white space
    split_list = []
    for term in query_terms:
        split = term.split()
        split_list = split_list + split

    query_terms = split_list

    avg_len = 0
    counter = 0
    sorted_drinks = {}

    #Get the average length per document
    for drink in drinks:
        ingredients = drink.ingredients.all()
        for ingredient in ingredients:
            avg_len += 1.0
        counter += 1.0
    avg_len /= counter

    #For each drink, get a score
    for drink in drinks:
        score = 0.0

        #Sum up all the terms to get the score
        for term in query_terms:
            term_freq = 0.0
            try:
                term_object = Frequency.objects.get(name=term.lower())
                term_freq = float(term_object.quantity)
            except ObjectDoesNotExist:
                term_freq = 0.0
	        #idf below
            idf = log((len(drinks)-term_freq+.5)/(term_freq+.5),2)
            ingredients = drink.ingredients.all()
            doc_freq = 0.0
            total_freq = 0.0
            for ingredient in ingredients:
                if (term.lower() in ingredient.name.lower()):
                    doc_freq += 1.0
                total_freq += 1.0
            #doc frequency below
            doc_freq /= total_freq
            #k, b below, |d| is total_freq
            b = 0.75
            k = 1.2
            numerator = doc_freq*(k + 1)*idf
            denominator = doc_freq + k*(1 - b + b * (total_freq/avg_len))
            score += numerator / denominator
        #print drink.name.encode('utf-8')
        #print 100-score
        sorted_drinks[drink] = 100-score
    sorted_dict = sorted(sorted_drinks.iteritems(), key=operator.itemgetter(1))
    #sorted_drinks = dict(sorted_dict)
    for drink in sorted_dict:
        print drink[0].name.encode('utf-8'), ":", drink[1]
    return sorted_dict
