from django.db import models

class Drink(models.Model):
    name = models.CharField(max_length=250)
    rating = models.IntegerField()
    num_ratings = models.IntegerField()
    directions = models.CharField(max_length=250)
    #tags = models.ManyToManyField("Tag")
    ingredients = models.ManyToManyField("Ingredient")
    class Meta:
        app_label = "drink"

    def __unicode__(self):
        return self.name


#class Tag(models.Model):

class Ingredient(models.Model):
    name = models.CharField(max_length=250)
    unit = models.CharField(max_length=250)
    amount = models.IntegerField()
    class Meta:
        app_label = "ingredient"

    def __unicode__(self):
        return self.name

