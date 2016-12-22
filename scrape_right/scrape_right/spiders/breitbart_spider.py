import scrapy
from scrape_right.items import Article


class BreitbartSpider(scrapy.Spider):
    name = 'breitbart'

    def start_requests(self):
        urls = [
            'http://www.breitbart.com/'
        ]

        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse_homepage)

    def parse_homepage(self, response):
        '''Parse home page looking for links. Schedule requests article URL
        and parse with parse_article
        '''

        for article in response.xpath('//article/a'):
            article_url = article.xpath('@href').extract_first()
            yield scrapy.Request(response.urljoin(article_url),
                                 callback=self.parse_article)

    def parse_article(self, response):
        '''Main function for parsing articles. Takes response from parse_homepage
        and yields Article item'''

        # Limit to main article body to avoid tag conflicts with other portions of page
        page = response.xpath('//div[contains(@id, "MainW")]')

        # Combine headling and text from <p> tags into one string
        def get_text_blob(page, headline):
            if page.xpath('//h2/text()').extract_first():
                blob = page.xpath('//h2/text()').extract_first()
            else:
                blob = ''
            for text in page.xpath('//p/text()'):
                blob = blob + text.extract()
            return blob

        # Create and return article item
        article = Article(
            language='en',
            url=response.url,
            authors=page.xpath('//a[contains(@class, "byauthor")]/text()').extract_first(),
            pub_datetime=page.xpath('//time[contains(@class, "published")]/@datetime').extract(),
            modified_datetime=page.xpath('//time[contains(@class, "modified")]/@datetime').extract(),
            title=page.xpath('//h1[contains(@itemprop, "headline")]/text()').extract_first(),
            headline=page.xpath('//h2/text()').extract_first(),
            text_blob=get_text_blob(page, False),

        )

        yield article
