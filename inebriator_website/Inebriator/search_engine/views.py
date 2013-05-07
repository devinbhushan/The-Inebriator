from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template.loader import get_template
from django.template import Context, RequestContext
from django.template.defaulttags import csrf_token
from models import *
from forms import *
from django.utils import simplejson
from django.core import serializers
from django.db.models import Q
from ranking import *
from client import Client
import json
from dictionary import Dictionary
#from django.conf import settings
#import sys

def home(request):
    """
    Home page of the website
    """
    return render_to_response('home.html')

def search(request, page=1):
    """
    Search page
    """
    print "dsdf %s" % request
    if request.POST:
        if request.is_ajax():
            print "ajax!"
        spell_check = Dictionary()
        spell_check.init_dict()

        required = request.POST.getlist('required[]')
        corrected_required = []
        for term in required:
            correct_term = spell_check.correct(term)
            corrected_required.append(correct_term)
        required = corrected_required

        optional = request.POST.getlist('optional[]')
        corrected_optional = []
        for term in optional:
            correct_term = spell_check.correct(term)
            corrected_optional.append(correct_term)
        optional = corrected_optional

        print "required: %s" % required
        drinks = []
        master_set = set(Drink.objects.all())
        if required:
            for term in required:
                results = Drink.objects.filter(
                                        Q(name__contains=term) |
                                        Q(ingredients__name__contains=term))
                master_set = master_set & set(results)
            drinks = list(master_set)
        else:
            for term in optional:
                drinks.extend(list(Drink.objects.
                                    filter(Q(name__contains=term) |
                                            Q(ingredients__name__contains=term))
                                .distinct()))
            drinks = list(set(drinks))

        if len(drinks)== 0:
            drinks_list = []
        else:
            drinks_tuple = rank(required+optional, drinks)
            drinks_list = []
            print "Starting views"
            for drink in drinks_tuple:
                drinks_list.append(drink[0])
                print "%s" % drink[0].name.encode('utf-8')
        json_drinks = []
        for drink in drinks_list:
            curr_drink = {}
            curr_drink["name"] = drink.name
            curr_drink["directions"] = drink.directions
            curr_drink["ingredients"] = []

            for ingredient in drink.ingredients.all():
                curr_ingredient = {}
                curr_ingredient["name"] = ingredient.name
                curr_ingredient["unit"] = ingredient.unit
                curr_ingredient["amount"] = ingredient.amount
                curr_drink["ingredients"].append(curr_ingredient)

            json_drinks.append(curr_drink)
        return HttpResponse(json.dumps(json_drinks), mimetype='application/json')#render_to_response('search.html', {'form': form,
                                                    #'results':drinks[(page-1)*500:page*500],
                                                    #'page':page,
                                                    #'next':page+1,
                                                    #'prev':page-1},
         #                           context_instance=RequestContext(request))

    else:
        form = Search_Form()
        return render_to_response('search.html', {'form': form},
                                  context_instance=RequestContext(request))

def raspberry(request):
    """
    Trending section of the website
    """
    client_obj = Client()
    client_obj.connect('192.168.1.105', 9999)
    client_obj.send("8======D~~~~~~~O:")
    pi_ingredients = json.loads(client_obj.listen())
    print "message received!: %s" % pi_ingredients

    master_set = set(Drink.objects.all())
    for ingredient in pi_ingredients:
        results = Drink.objects.filter(
                                Q(ingredients__name__contains=ingredient))
        master_set = master_set & set(results)
    drinks = list(master_set)

    if len(drinks)== 0:
            drinks_list = []
    else:
        drinks_tuple = rank(pi_ingredients, drinks)
        drinks_list = []
        print "Starting views"
        for drink in drinks_tuple:
            drinks_list.append(drink[0])
            print "%s" % drink[0].name.encode('utf-8')

    return render_to_response('raspberry.html', {'msg':drinks_list})

def popular(request):
    """
    Popular section of the website
    """
    return render_to_response('popular.html')
