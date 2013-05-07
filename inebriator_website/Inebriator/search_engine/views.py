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
        required = request.POST.getlist('required[]')
        optional = request.POST.getlist('optional[]')
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
        return HttpResponse(serializers.serialize("json",drinks_list), mimetype='application/json')#render_to_response('search.html', {'form': form,
                                                    #'results':drinks[(page-1)*500:page*500],
                                                    #'page':page,
                                                    #'next':page+1,
                                                    #'prev':page-1},
         #                           context_instance=RequestContext(request))

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
