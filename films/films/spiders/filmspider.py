import scrapy


class FilmspiderSpider(scrapy.Spider):
    name = 'filmspider'
    allowed_domains = ['ru.wikipedia.org']
    start_urls = ['https://ru.wikipedia.org/w/index.php?title=%D0%9A%D0%B0%D1%82%D0%B5%D0%B3%D0%BE%D1%80%D0%B8%D1%8F%3A%D0%A4%D0%B8%D0%BB%D1%8C%D0%BC%D1%8B_%D0%BF%D0%BE_%D0%B0%D0%BB%D1%84%D0%B0%D0%B2%D0%B8%D1%82%D1%83&from=%D0%90']

    def parse(self, response):
        titles = response.css('div.mw-category-group ul li')
        for title in titles:
            title_url = 'https://ru.wikipedia.org' + title.css('a::attr(href)').get()
            yield response.follow(title_url, callback=self.parse_film)
        
        next_page = response.css('div.mw-category-generated a::attr(href)')[-1].get()  
        if next_page is not None:
            next_page_url = 'https://ru.wikipedia.org' + next_page
            yield response.follow(next_page_url, callback=self.parse)

    
    def parse_film(self, response):
            table_rows = response.css('table tr')
            if table_rows.css('span[data-wikidata-property-id="P577"] ::text').get() is None:
                 year = table_rows.css('span[class="dtstart"] ::text').get()
            yield {
                 'title' : table_rows[0].css('::text').get(),
                 'genre' : ', '.join(table_rows.css('span[data-wikidata-property-id="P136"] ::attr(title)').getall()).strip('"'),
                 'director' : ', '.join(table_rows.css('span[data-wikidata-property-id="P57"] ::attr(title)').getall()).strip('"'),
                 'country' : ', '.join(table_rows.css('span[data-wikidata-property-id="P495"] ::attr(data-sort-value)').getall()).strip('"'),
                 'year' : year,
            }
            
            
            
            
            
            



