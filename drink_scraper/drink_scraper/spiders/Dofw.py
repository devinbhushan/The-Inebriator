from scrapy.spider import BaseSpider
from scrapy.selector import HtmlXPathSelector
from drink_scraper.items import Drink
from scrapy import log


class Dofw(BaseSpider):
    '''
    Spider for http://www.drinkoftheweek.com/list-drinks-a-z/
    '''
    name = "dofw"
    allowed_domains = ["drinkoftheweek.com"]
    start_urls = ["http://www.drinkoftheweek.com/list-drinks-a-z/"]

    def parse(self, response):
        log.msg("Beginning parse function", level=log.INFO)
        hxs = HtmlXPathSelector(response)
        outer_links = hxs.select("//div[@class='alpha_drink_list']/ul[@class='drinkgroup']/li")
        log.msg('number outer_links: %s' % len(outer_links), level=log.INFO)
        for outer_link in outer_links:
            links = outer_links.select('a/@href').extract()
            for link in links:
                # TODO Go to each link and collect info per drink
                print link
                return
        pass
