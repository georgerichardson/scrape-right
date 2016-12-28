import scrapy
from scrape_right.items import Article
from scrapy import Request

class BreitbartSpider(scrapy.spiders.CrawlSpider):
    '''Breitbart news spider

    Arguments:
    limit -- Pagination limit where crawler will stop. There are approximately 30-35
    articles per page. (Default=0 will only search frontpage). Example: limit=5
    will search 5 pages of archives for all news categories found on Breitbart
    front page ~1500 articles

    Example Command: scrapy crawl breitbart -o <outputfile.json> -a limit=5 --logfile <logfile.txt>
    '''

    name = 'breitbart'

    def __init__(self, limit=0, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.limit = int(limit)



    def start_requests(self):
        urls = ['http://www.breitbart.com']

        # main landing page only
        if self.limit == 0:
            for url in urls:
                yield scrapy.Request(url=url, callback=self.parse_landing_page)

        # crawl all subsections
        else:
            for url in urls:
                yield scrapy.Request(url=url, callback=self.search_categories)

    def search_categories(self, response):

        # Menu bar found at top of page contains sub-sections of site
        menu_bar = response.xpath('//ul[contains(@class, "menu")]')[0:2]  # bottom bar is duplicate
        for menu in menu_bar:
            category_list = menu.xpath('.//a/@href').extract()
            for category in category_list:
                yield scrapy.Request(response.urljoin(category),
                                     callback=self.parse_landing_page)

    def parse_landing_page(self, response):
        # pagination get "older posts" href
        next_page = response.xpath('//div[@class="pagination"]/div/a/@href').extract_first()

        # main section
        page = response.xpath('//div[contains(@id, "MainW")]')

        for article in page.xpath('//article/a'):
            article_url = article.xpath('@href').extract_first()
            yield Request(response.urljoin(article_url),
                          callback=self.parse_article)

        if next_page:
            if int(next_page.split('/')[-2]) <= self.limit:
                yield scrapy.Request(response.urljoin(next_page),
                                     callback=self.parse_landing_page)


    def parse_article(self, response):
        '''Main function for parsing articles. Takes article URLS and yields
        Article item
        '''

        # Limit to main article body to avoid tag conflicts with other portions of page
        body = response.xpath('//div[contains(@id, "MainW")]')

        # Helper function to combine lead plus text body into one string
        def get_text_blob(body):

            # this is the lead
            if body.xpath('//h2/text()').extract_first():
                blob = body.xpath('//h2/text()').extract_first()
            # no lead
            else:
                blob = ''

            for text in body.xpath('//p/text()'):
                blob = blob + text.extract()
            return blob

        article = Article(
            language=response.xpath('/html/@lang').extract_first(),
            url=response.url,
            authors=body.xpath('//a[contains(@class, "byauthor")]/text()').extract_first(),
            pub_datetime=body.xpath('//time[contains(@class, "published")]/@datetime').extract_first(),
            modified_datetime=body.xpath('//time[contains(@class, "modified")]/@datetime').extract_first(),
            title=body.xpath('//h1[contains(@itemprop, "headline")]/text()').extract_first(),
            lead=body.xpath('//h2/text()').extract_first(),
            text_blob=get_text_blob(body),
            source='breitbart',

        )

        yield article
