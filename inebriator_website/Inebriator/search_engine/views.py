from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template.loader import get_template
from django.template import Context, RequestContext
from django.template.defaulttags import csrf_token
from models import *
from forms import *
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
            cd = form.cleaned_data
            search = cd['search']
            terms = search.split()
            drinks = []
            for term in terms:
                drinks.extend(list(Drink.objects.filter(name__contains=term).distinct()))
            drinks = list(set(drinks))
            if len(drinks)== 0:
                drinks = "None"
            return render_to_response('search.html', {'form': form,
                                                      'results':drinks[(page-1)*500:page*500],
                                                      'page':page,
                                                      'next':page+1,
                                                      'prev':page-1},
                                      context_instance=RequestContext(request))
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
