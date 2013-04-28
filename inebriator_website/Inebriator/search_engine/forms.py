from django import forms
from models import *

# Examples
#class BlogCreate(forms.ModelForm):
    #class Meta:
        #model = BlogEntry
        #exclude = ('publish_date', 'slug')

#class CategoryCreate(forms.ModelForm):
    #class Meta:
        #model = Category
#        exclude = ('slug')

class Search_Form(forms.Form):
    #search = forms.CharField(max_length=100, required=False, label="Drink Name")
    search = forms.CharField(label="", widget=forms.TextInput(attrs={'class': 'hidden'}))
    optional = forms.CharField(label="", widget=forms.TextInput(attrs={'class': 'hidden'}))
    #optional = forms.CharField(widget=forms.HiddenInput(), label="filter")

#    def __init__(self, *args, **kwargs):
        #num_ingredients = kwargs.pop('num_ingredients',1)
        #super(Search_Form, self).__init__(*args, **kwargs)

        #for ingredient in range(0, num_ingredients):
            #field = forms.CharField(label="Ingredient")
#            self.fields[str(ingredient)] = field
