import scrapy
import json


class QuotesSpider(scrapy.Spider):
    name = 'quotes'
    start_urls = ['http://quotes.toscrape.com/']

    def parse(self, response):
        quotes = []
        authors = {}

        for quote in response.css('div.quote'):
            quote_data = {
                'text': quote.css('span.text::text').get(),
                'author': quote.css('span small.author::text').get(),
                'tags': quote.css('div.tags a.tag::text').getall(),
            }
            quotes.append(quote_data)

            author_name = quote_data['author']
            if author_name not in authors:
                authors[author_name] = {'name': author_name}

        with open('quotes.json', 'w') as f:
            json.dump(quotes, f, indent=2)

        with open('authors.json', 'w') as f:
            author_list = list(authors.values())
            json.dump(author_list, f, indent=2)

        next_page = response.css('li.next a::attr(href)').get()
        if next_page is not None:
            yield response.follow(next_page, self.parse)