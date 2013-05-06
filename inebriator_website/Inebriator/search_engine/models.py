from django.db import models


class Drink(models.Model):
    name = models.CharField(max_length=250, primary_key=True)
    rating =  models.CharField(max_length=250, null=True)
    num_ratings =  models.CharField(max_length=250, null=True)
    directions = models.TextField()
    #tags = models.ManyToManyField("Tag")
    ingredients = models.ManyToManyField("Ingredient")

    class Meta:
        app_label = "search_engine"

    def __unicode__(self):
        return self.name


#class Tag(models.Model):

class Ingredient(models.Model):
    name = models.CharField(max_length=250)
    unit = models.CharField(max_length=250, null=True)
    amount = models.CharField(max_length=250, null=True)

    class Meta:
        app_label = "search_engine"

    def __unicode__(self):
        return self.name

class Frequency(models.Model):
    name = models.CharField(max_length=250, primary_key=True)
    quantity = models.DecimalField(max_digits=25,decimal_places=24)

    class Meta:
        app_label = "search_engine"

    def __unicode__(self):
        return self.name
