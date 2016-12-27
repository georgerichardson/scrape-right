from scrape_right.items import Article
from scrapy.spiders import CrawlSpider, Rule
from scrapy import Request
from scrapy.linkextractors.lxmlhtml import LxmlLinkExtractor


class BreitbartSpider2(CrawlSpider):
    name = 'breitbart2'

    allowed_domains = ['breitbart.com']
    start_urls = ["http://www.breitbart.com/"]

    rules = (
        Rule(LxmlLinkExtractor(restrict_xpaths=('//div[@id="HWI"]/nav/ul[@class="menu"]')),
             ),

        Rule(LxmlLinkExtractor(restrict_xpaths=('//div[@class="pagination"]')),
             callback='parse_landing_page', follow=True)
        )

    def parse_landing_page(self, response):
        '''Parse landing page looking for articles. Schedule requests to article URL
        and submit to parse_article
        '''

        # Limit to main article body to avoid tag conflicts with other portions of page
        page = response.xpath('//div[contains(@id, "MainW")]')

        # search landing page for articles
        for article in page.xpath('//article/a'):
            article_url = article.xpath('@href').extract_first()
            yield Request(response.urljoin(article_url),
                          callback=self.parse_article)

    def parse_article(self, response):
        '''Main function for parsing articles. Takes article URLS and yields
        Article item
        '''

        # Limit to main article body to avoid tag conflicts with other portions of page
        page = response.xpath('//div[contains(@id, "MainW")]')

        # Helper function to combine lead plus text body into one string
        def get_text_blob(page):

            # this is the lead
            if page.xpath('//h2/text()').extract_first():
                blob = page.xpath('//h2/text()').extract_first()
            # no lead
            else:
                blob = ''

            for text in page.xpath('//p/text()'):
                blob = blob + text.extract()
            return blob

        article = Article(
            language=response.xpath('/html/@lang').extract_first(),
            url=response.url,
            authors=page.xpath('//a[contains(@class, "byauthor")]/text()').extract_first(),
            pub_datetime=page.xpath('//time[contains(@class, "published")]/@datetime').extract_first(),
            modified_datetime=page.xpath('//time[contains(@class, "modified")]/@datetime').extract_first(),
            title=page.xpath('//h1[contains(@itemprop, "headline")]/text()').extract_first(),
            lead=page.xpath('//h2/text()').extract_first(),
            text_blob=get_text_blob(page),
            source='breitbart',

        )

        yield article
