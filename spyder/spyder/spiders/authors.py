import scrapy
import json
import urllib.parse


class AuthorsSpider(scrapy.Spider):
    name = 'authors'
    allowed_domains = ['quotes.toscrape.com']
    start_urls = []

    custom_settings = {
        'FEED_FORMAT': 'json',
        'FEED_URI': 'authors.json'
    }

    def __init__(self, *args, **kwargs):
        super(AuthorsSpider, self).__init__(*args, **kwargs)
        with open('quotes.json', 'r', encoding='utf-8') as f:
            quotes = json.load(f)
            authors = {quote['author'] for quote in quotes}
            self.start_urls = [
                self.format_author_url(author) for author in authors
            ]

    def format_author_url(self, author):
        formatted_author = (author.replace(' ', '-')
                                   .replace('.', '-')
                                   .replace('--', '-')
                                   .replace('é', 'e')
                                   .replace("'", "")
                                   .rstrip('-'))
        return f"http://quotes.toscrape.com/author/{urllib.parse.quote(formatted_author)}/"

    def parse(self, response):
        fullname = response.xpath("//h3[@class='author-title']/text()").get()
        born_date = response.xpath("//span[@class='author-born-date']/text()").get()
        born_location = response.xpath("//span[@class='author-born-location']/text()").get()
        description = response.xpath("//div[@class='author-description']/text()").get()

        self.log(f"Scraping author page: {response.url}")
        self.log(f"fullname: {fullname}")
        self.log(f"born_date: {born_date}")
        self.log(f"born_location: {born_location}")
        self.log(f"description: {description}")

        yield {
            "fullname": fullname.strip() if fullname else '',
            "born_date": born_date.strip() if born_date else '',
            "born_location": born_location.strip() if born_location else '',
            "description": description.strip() if description else ''
        }
