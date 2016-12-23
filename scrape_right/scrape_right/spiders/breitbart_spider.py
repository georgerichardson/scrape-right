import scrapy
from scrape_right.items import Article


class BreitbartSpider(scrapy.Spider):
    name = 'breitbart'

    def start_requests(self):
        urls = [
            'http://www.breitbart.com/'
        ]

        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse_url)

    def parse_url(self, response):
        '''Parse top nav bar for major categories. Schedule requests to each category
        landing page and call parse_landing_page
        '''

        # Menu bar found at top of page contains sub-sections of site
        menu_bar = response.xpath('//ul[contains(@class, "menu")]')[0:2]  # bottom bar is duplicate
        for menu in menu_bar:
            category_list = menu.xpath('.//a/@href').extract()
            for category in category_list:
                yield scrapy.Request(response.urljoin(category),
                                     callback=self.parse_landing_page)

    def parse_landing_page(self, response):
        '''Parse landing page looking for articles. Schedule requests to article URL
        and submit to parse_article
        '''

        # search landing page for articles
        for article in response.xpath('//article/a'):
            article_url = article.xpath('@href').extract_first()
            yield scrapy.Request(response.urljoin(article_url),
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
