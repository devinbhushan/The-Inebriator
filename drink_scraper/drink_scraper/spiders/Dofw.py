from scrapy.spider import BaseSpider
from scrapy.selector import HtmlXPathSelector
from drink_scraper.items import Drink
from scrapy import log
from scrapy.http import Request
from drink_scraper.unit_analyzer import Unit_Analyzer


class Dofw(BaseSpider):
    """
    Spider for http://www.drinkoftheweek.com/list-drinks-a-z/
    """
    name = "dofw"
    allowed_domains = ["drinkoftheweek.com"]
    start_urls = ["http://www.drinkoftheweek.com/list-drinks-a-z/"]

    def parse(self, response):
        """
        Parse function to get each drink's link and parse it
        """
        log.msg("Beginning parse function", level=log.INFO)
        hxs = HtmlXPathSelector(response)
        outer_links = hxs.select("//div[@class='alpha_drink_list']/ul[@class='drinkgroup']/li")
        log.msg('number outer_links: %s' % len(outer_links), level=log.INFO)

        for outer_link in outer_links:
            links = outer_links.select('a/@href').extract()
            for link in links:
                #log.msg('following %s' % link, level=log.INFO)
                yield Request(link, callback=self.parseDrink)

    def parseDrink(self, response):
        """
        Parse function to go grab Drink info from each drink
        Returns Drink Item
        """
        hxs = HtmlXPathSelector(response)
        drink = Drink()

        drink['name'] = hxs.select("//h2[@class='pagetitle']/text()").extract()[0]
        drink['rating'] = hxs.select("//meta[@itemprop='ratingValue']/@content").extract()[0]
        drink['num_reviews'] = hxs.select("//meta[@itemprop='ratingCount']/@content").extract()[0]

        drink['tags'] = []
        tags = hxs.select("//div[@class='posttags']/a[@rel='tag']")
        for tag in tags:
            drink['tags'].append(tag.select("text()").extract()[0])

        drink['ingredients'] = []
        unit_analyzer = Unit_Analyzer()
        ingredient_strings = hxs.select("//ul[@class='ingredients']/li")
        for ingredient_string in ingredient_strings:
            final_triple = unit_analyzer.get_triple(ingredient_string.select('text()').extract()[0])
            drink['ingredients'].append(final_triple)

        log.msg('Drink retrieved: %s' % drink, level=log.INFO)
        return drink
