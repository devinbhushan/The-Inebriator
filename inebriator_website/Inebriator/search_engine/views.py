from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template.loader import get_template
from django.template import Context, RequestContext
from django.template.defaulttags import csrf_token
from models import *
from forms import *
from django.db.models import Q
from ranking import *
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
    if request.method == "POST":
        form = Search_Form(request.POST)
        if form.is_valid():

            # Get information from the form
            cd = form.cleaned_data
            search = cd['search']
            terms = search.split()

            # Query for drinks with terms matching drink or
            # ingredients.
            drinks = []
            for term in terms:
                drinks.extend(list(Drink.objects.
                                   filter(Q(name__contains=term) |
                                          Q(ingredients__name__contains=term))
                                   .distinct()))
            drinks = list(set(drinks))

            # There are no drinks. Return no results
            #if drinks.qsize() == 0:
            if len(drinks) == 0:
                drinks_list = "None"
            else:
                drinks_tuple = rank(terms, drinks)
                drinks_list = []
                for drink in drinks_tuple:
                    drinks_list.append(drink[0])


            """
            drinks_list = []
            while not drinks.empty():
                drink = drinks.get()
                #print drink.name
                drinks_list.append(drink)
            """

            # Pass in results and render the html page
            return render_to_response('search.html', {'form': form,
                                                      'results':drinks_list[(page-1)*500:page*500],
                                                      'page':page,
                                                      'next':page+1,
                                                      'prev':page-1},
                                      context_instance=RequestContext(request))
    # The user has not made a query
    else:
        form = Search_Form()
        return render_to_response('search.html', {'form': form},
                                  context_instance=RequestContext(request))

def trending(request):
    """
    Trending section of the website
    """
    return render_to_response('trending.html')

def popular(request):
    """
    Popular section of the website
    """
    return render_to_response('popular.html')
