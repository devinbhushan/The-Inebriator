from scrapy.spider import BaseSpider
from scrapy.selector import HtmlXPathSelector
from drink_scraper.items import Drink
from scrapy import log
from scrapy.http import Request

'''proving devin wrong'''

class AR(BaseSpider):
    """
    Spider for http://allrecipes.com/recipes/drinks/ViewAll.aspx
    """
    name = "AR"
    allowed_domains = ["allrecipes.com"]
    start_urls = ["http://allrecipes.com/recipes/drinks/ViewAll.aspx"]

    def parse(self, response):
        """
        Parse function to get each drink's link and parse it
        @Retur
        """
        log.msg("Beginning parse function", level=log.INFO)
        hxs = HtmlXPathSelector(response)
        outer_links = hxs.select("//div[@class='yay']/div[@class='recipes recipies_compact']")
        log.msg('number outer_links: %s' % len(outer_links), level=log.INFO)
        #table//h3/a/@href
        for outer_link in outer_links:
            links = outer_links.select('table//h3/a/@href').extract()
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

        drink['name'] = hxs.select("//h1[@class='plaincharcterwrap']/text()")
        drink['rating'] = hxs.select("//meta[@itemprop='ratingValue']/@content")
        drink['num_reviews'] = hxs.select("//meta[@itemprop='metaReviewCount']/@content")
        drink['directions'] = []
        directionlist = hxs.select("//div[@class='directLeft']/ol/li")
        
        for list in directionlist:
                drink['directions'].append(list.select("span/text()"))
        
        

        drink['tags'] = None
        ''' tags = hxs.select("//div[@class='posttags']/a[@rel='tag']")
        for tag in tags:
            drink['tags'].append(tag.select("text()"))
        '''
        log.msg('Drink retrieved: %s' % drink, level=log.INFO)
        return drink               
                
                
                
                
                
                