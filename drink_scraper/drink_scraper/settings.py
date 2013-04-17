# Scrapy settings for drink_scraper project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/topics/settings.html
#

BOT_NAME = 'drink_scraper'

SPIDER_MODULES = ['drink_scraper.spiders']
NEWSPIDER_MODULE = 'drink_scraper.spiders'

# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'drink_scraper (+http://www.yourdomain.com)'
