from scrapy.spider import BaseSpider
from scrapy.selector import HtmlXPathSelector
from drink_scraper.items import Drink
from scrapy import log
from scrapy.http import Request
from drink_scraper.unit_analyzer import Unit_Analyzer
from string import ascii_lowercase


class Drinks_Mixer(BaseSpider):
    """
    Spider for http://www.drinkoftheweek.com/list-drinks-a-z/
    """
    name = "Drinks_Mixer"
    allowed_domains = ["drinksmixer.com"]
    #start_urls = ["http://www.drinksmixer.com/cat/j/"]

    def start_requests(self):
        for letter in ascii_lowercase:
            url = "http://www.drinksmixer.com/cat/" + letter + "/"
            yield self.make_requests_from_url(url)

    def parse(self, response):
        """
        Parse function to get each drink's link and parse it
        """
        log.msg("Beginning parse function", level=log.INFO)
        hxs = HtmlXPathSelector(response)
        outer_links = hxs.select("//div[@class='l1a']")
        #log.msg('number outer_links: %s' % len(outer_links), level=log.INFO)

        drinks_retrieved = 0
        for outer_link in outer_links:
            links = outer_links.select('a/@href').extract()
            for link in links:
                link = "http://www.drinksmixer.com" + link
                #log.msg('following %s' % link, level=log.INFO)
                yield Request(link, callback=self.parseDrink)
                drinks_retrieved += 1
        #log.msg('drinks retrieved: %d' % drinks_retrieved, level=log.INFO)

    def parseDrink(self, response):
        """
        Parse function to go grab Drink info from each drink
        Returns Drink Item
        """
        hxs = HtmlXPathSelector(response)
        drink = Drink()

        #Get names and ratings
        drink['name'] = hxs.select("//h1[@class='fn recipe_title']/text()").extract()[0]
        drink['rating'] = hxs.select("//div[@class='ratingsBox rating']/div[1]/div[1]/text()").extract()
        drink['num_reviews'] = hxs.select("//div[@class='ratingsBox rating']//span[@class='count']/text()").extract()

        #If no rating, make None
        if len(drink['rating'][0]) > 4:
            drink['rating'] = None
            drink['num_reviews'] = None

        # Print for Error checking
        #log.msg('name: %s' % drink['name'], level=log.INFO)
        #log.msg('rating: %s' % drink['rating'], level=log.INFO)
        #log.msg('num_reviews: %s' % drink['num_reviews'], level=log.INFO)

        #drink['tags'] = []
        #tags = hxs.select("//div[@class='posttags']/a[@rel='tag']")
        #for tag in tags:
        #    drink['tags'].append(tag.select("text()").extract()[0])

        drink['tags'] = None

        #Get Ingredients. Turn into string that is parsable by unit_analyzer
        drink['ingredients'] = []
        unit_analyzer = Unit_Analyzer()
        ingredient_strings = hxs.select("//div[@class='ingredients']//span[@class='ingredient']")
        for ingredient_string in ingredient_strings:
            full_string = ingredient_string.select(".//span[@class='amount']/text()").extract()[0]
            #log.msg('amount: %s' % full_string, level=log.INFO)
            full_string += " " + ingredient_string.select(".//span[@class='name']//a/text()").extract()[0]
            #log.msg('ingredient: %s' % full_string, level=log.INFO)
            final_triple = unit_analyzer.get_triple(full_string)
            drink['ingredients'].append(final_triple)

        #Directions
        drink['directions'] = hxs.select("//div[@class='RecipeDirections instructions']/text()").extract()

        #log.msg('Drink retrieved: %s' % drink, level=log.INFO)
        return drink
