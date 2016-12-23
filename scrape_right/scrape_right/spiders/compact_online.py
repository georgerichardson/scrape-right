import scrapy
from scrape_right.items import Article
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor


class CompactOnline(CrawlSpider):
    name = 'compact'

    allowed_domains = ['compact-online.de']
    start_urls = ["http://www.compact-online.de"]

    rules = (
        Rule(LinkExtractor(allow_domains=allowed_domains), 
             callback='parse_article', follow=True
            ),
        )

    def parse_article(self, response):
        '''Main function for parsing articles. Takes response from parse_homepage
        and yields Article item'''

        # Combine text from <p> tags into one string
        def get_text_blob(response):
            blob = ''
            for text in response.xpath('//div[contains(@class, "post-content description ")]//p/text()'):
                blob = ''.join([blob,text.extract()])
            return blob

        # Get page type to see if page is an article
        try: 
            page_type = response.xpath("//meta[@property='og:type']/@content").extract()[0] 
        except:
            pass

        if page_type == "article":
            # Create and return article item
            article = Article(
                language='de',
                url=response.url,
                authors=response.xpath('//a[contains(@rel, "author")]/text()').extract_first(),
                pub_datetime=response.xpath("//meta[@property='article:published_time']/@content").extract_first(),
                title=response.xpath("//meta[@property='og:title']/@content").extract_first(),
                text_blob=get_text_blob(response),
                source="compact-online"

            )

            yield article
