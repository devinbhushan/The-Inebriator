from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template.loader import get_template
from django.template import Context, RequestContext
from models import *
#from forms import *
#from django.conf import settings
#import sys

def home(request):
    """
    Home page of the website
    """
    return render_to_response('home.html')

def search(request):
    """
    Search page
    """
    return render_to_response('search.html')

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
