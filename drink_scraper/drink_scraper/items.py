# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/topics/items.html

from scrapy.item import Item, Field


class Drink(Item):
    '''
    name = String
    ingredients = [(quantity, name, unit), ..., (quantity_last, name_last, unit_last)]
    rating = Integer
    num_reviews = Integer
    directions = [String, String, String]
    tags = [String, String, String]
    Example:
        name = "Admiral"
        ingredients = [(1, bourbon, oz), (1, dry vermouth, oz), ...]
        rating = 4.67
        num_reviews = 3
        directions = ["Step1", "Step2", "Step3"]
        tags = ["bourbon", "dry_vermouth", "lemon", "lemon juice", ...]
    '''
    name = Field()
    ingredients = Field()
    num_reviews = Field()
    directions = Field()
    rating = Field()
    tags = Field()
