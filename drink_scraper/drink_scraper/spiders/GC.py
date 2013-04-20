from scrapy.spider import BaseSpider
from scrapy.selector import HtmlXPathSelector
from items import Drink
from scrapy import log
from scrapy.http import Request
 
 
class GC(BaseSpider):
    """ 
    Spider for Good Cocktails
    """
    name = "gc"
    allowed_domains = ["goodcocktails.com"]
    start_urls = ["http://www.goodcocktails.com/recipes/browse_drinks.php?letter=ALL"]

    def parse(self, response):
        """ 
        Parse function to get each drink's link and parse it
        """
        log.msg("Beginning parse function", level=log.INFO)
        hxs = HtmlXPathSelector(response)
        outer_links = hxs.select("//div[@id='drinkList']/ul/li")
        log.msg('number outer_links: %s' % len(outer_links), level=log.INFO)

        for outer_link in outer_links:
            links = outer_links.select('a/@href').extract()
            for link in links:
                #log.msg('following %s' % link, level=log.INFO)
                yield Request("http://www.goodcocktails.com/recipes/" + link, callback=self.parseDrink)

    def parseDrink(self, response):
        """
        Parse function to go grab Drink info from each drink
        Returns Drink Item
        """
        hxs = HtmlXPathSelector(response)
        drink = Drink()

        drink['name'] = hxs.select("//div[@id='drinkRecipe']/h2/text()").extract()[0]
        drink['rating'] = None
        drink['num_reviews'] = None
        drink['tags'] = None
        drink['directions'] = hxs.select("//div[@id='drinkRecipe']/p[position()=2]").extract()[0]
        drink['ingredients'] = []
        unit_analyzer = Unit_Analyzer()
        ingredient_strings = hxs.select("//div[@id='drinkRecipe']/ul/li")
        for ingredient_string in ingredient_strings:
            final_triple = unit_analyzer.get_triple(ingredient_string.select('text()').extract()[0])
            drink['ingredients'].append(final_triple)

        log.msg('Drink retrieved: %s' % drink, level=log.INFO)
        return drink
